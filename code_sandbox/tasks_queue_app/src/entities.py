import enum
from typing import Callable, Dict, Optional, Protocol, runtime_checkable

from . import tasks
from ... import utils

__all__ = [
    "create_event_pool",
    "EntityEvents",
    "Entity",
    "Manager",
    "Worker",
]


class EntityEvents(enum.Enum):
    Update = "Update Event"
    AfterUpdate = "After Update Event"

    GetTask = "Get Task Event"
    DisposeTask = "Dispose Task Event"

    Log = "Log Event"


def create_event_pool() -> Dict[enum.Enum, utils.Event]:
    event_pool = {
        EntityEvents.Update: utils.Event(),
        EntityEvents.AfterUpdate: utils.Event(),
        EntityEvents.GetTask: utils.Event(),
        EntityEvents.Log: utils.Event(),
    }

    task_disposition_event = utils.Event()
    task_disposition_event.event_distribution = utils.ForFirstToTakeDistribution()
    event_pool[EntityEvents.DisposeTask] = task_disposition_event
    return event_pool


@runtime_checkable
class SupportsUpdates(Protocol):
    def update(self):
        raise NotImplementedError

    def after_update(self):
        raise NotImplementedError


@runtime_checkable
class SupportsWorking(Protocol):
    _current_task: Optional[tasks.Task]

    @property
    def is_busy(self) -> bool:
        return self._current_task is not None

    def work_on(self, task: tasks.Task) -> None:
        raise NotImplementedError


@runtime_checkable
class SupportsTaskManagement(Protocol):
    @property
    def can_collect_task(self) -> bool:
        raise NotImplementedError

    def dispose_task(self) -> Optional[tasks.Task]:
        raise NotImplementedError

    def collect_task(self, task_pool: tasks.TaskPool) -> None:
        raise NotImplementedError


class Entity(SupportsUpdates):
    _event_pool: Dict[enum.Enum, utils.Event]
    _name: str

    def __init__(self, name: str) -> None:
        self._event_pool = {}
        self._name = name

    def __str__(self) -> str:
        return self.name

    @property
    def name(self) -> str:
        return self._name

    def update(self):
        pass

    def after_update(self):
        pass

    def subscribe(self, event_pool: Dict[enum.Enum, utils.Event]) -> None:
        self._event_pool = event_pool
        self._event_pool[EntityEvents.Update].attach(self.update)
        self._event_pool[EntityEvents.AfterUpdate].attach(self.after_update)

    def unsubscribe(self) -> None:
        self._event_pool[EntityEvents.Update].detach(self.update)
        self._event_pool[EntityEvents.AfterUpdate].detach(self.after_update)
        self._event_pool = {}

    def log(self, msg: str) -> None:
        self._event_pool[EntityEvents.Log](msg)


class Worker(Entity, SupportsWorking):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._current_task = None

    def __repr__(self):
        return f'Worker("{self.name}")'

    def update(self) -> None:
        msgs = []
        if self._current_task and self._current_task.is_done:
            msgs.append(f"done {self._current_task}")
            self._current_task = None

        if not self.is_busy and self._event_pool[EntityEvents.DisposeTask].attach(
            self.work_on
        ):
            msgs.append(f"queued for next task")

        if msgs:
            self.log(f"{self} {' and '.join(msgs)}")

    def work_on(self, task: tasks.Task) -> None:
        self._event_pool[EntityEvents.DisposeTask].detach(self.work_on)
        self._current_task = task
        self._current_task.start()
        self.log(
            f"{self} starts working on {task} (est. time: {task.seconds_to_finish:.2f}s)"
        )


class Manager(Entity, SupportsTaskManagement):
    _task_pool: tasks.TaskPool
    _task_queue_len: int
    _did_task_disposition: bool

    def __init__(self, name: str) -> None:
        super().__init__(name)

        self._task_pool = tasks.TaskPool()
        self._task_queue_len = 1
        self._did_task_disposition = False

    def __repr__(self):
        return f'Manager("{self.name}")'

    @property
    def max_queued_tasks(self) -> int:
        """Maximum amount of tasks to collect. For no limit, set to 0"""
        return self._task_queue_len

    @max_queued_tasks.setter
    def max_queued_tasks(self, value: int) -> None:
        self._task_queue_len = max(0, int(value))

    def update(self) -> None:
        if self.can_collect_task:
            self._event_pool[EntityEvents.GetTask].attach(self.collect_task)

        if self._task_pool:
            self.dispose_task()

    def after_update(self) -> None:
        if not self._did_task_disposition:
            return

        # this assures that manager waits for another managers to dispose their tasks
        self.rejoin_event_queue(self.update, EntityEvents.Update)
        self._did_task_disposition = False

    def rejoin_event_queue(self, subscriber: Callable, event: EntityEvents) -> None:
        self._event_pool[event].detach(subscriber)
        self._event_pool[event].attach(subscriber)
        self.log(f"{self} moved to the end of the {event.value} queue")

    @property
    def can_collect_task(self) -> bool:
        return self.max_queued_tasks and len(self._task_pool) < self.max_queued_tasks

    def dispose_task(self) -> Optional[tasks.Task]:
        task = self._task_pool.get()
        if not task:
            return None

        self._did_task_disposition = self._event_pool[EntityEvents.DisposeTask](task)
        if not self._did_task_disposition:
            return None

        self._task_pool.remove(task)
        self.log(f"{self} disposed {task} successfully")
        return task

    def collect_task(self, task_pool: tasks.TaskPool) -> None:
        if not self.can_collect_task:
            self._event_pool[EntityEvents.GetTask].detach(self.collect_task)
            return None

        task = task_pool.pop()
        if not task:
            return None

        self._task_pool.put(task)
        self.log(
            f"{self} collected {task} | tasks to dispose: "
            f"{[str(task) for task in self._task_pool]}"
        )
