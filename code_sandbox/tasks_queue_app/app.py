import enum
import time
from typing import Any, Callable, Dict, Iterable, List, Optional, Protocol

from . import tasks
from .. import utils


class SupportsUpdates(Protocol):
    def update(self):
        pass

    def after_update(self):
        pass


class SupportsWorking(Protocol):
    def work_on(self, task: tasks.Task) -> None:
        pass


class EventNames(enum.Enum):
    Update = enum.auto()
    AfterUpdate = enum.auto()

    DisposeTask = enum.auto()


class App:
    _events: Dict[EventNames, utils.Event]

    _tasks_pool: List[tasks.Task]
    _start_time: float

    def __init__(self) -> None:
        self._start_time = time.time()
        self._events = {
            EventNames.Update: utils.Event(),
            EventNames.AfterUpdate: utils.Event(),
        }

        dispose_task_event = utils.Event()
        dispose_task_event.event_distribution = utils.ForFirstToTakeDistribution()
        self._events[EventNames.DisposeTask] = dispose_task_event

        self._tasks_pool = []

    def log(self, message: Any) -> None:
        print(f"Time: {time.time() - self._start_time:.2f}s | {message}")

    def run(self) -> None:
        self._events[EventNames.Update]()
        self._events[EventNames.AfterUpdate]()

    def subscribe(self, name: EventNames, fun: Callable) -> None:
        self._events[name].attach(fun)

    def unsubscribe(self, name: EventNames, fun: Callable) -> None:
        self._events[name].detach(fun)

    def load_tasks(self, tasks_iterable: Iterable[tasks.Task]) -> None:
        self._tasks_pool += list(tasks_iterable)

    def get_task(self) -> Optional[tasks.Task]:
        if not self._tasks_pool:
            return None

        return self._tasks_pool.pop()

    def join_task_disposition(self, obj_: SupportsWorking) -> bool:
        if obj_.work_on in self._events[EventNames.DisposeTask]:
            return False

        self._events[EventNames.DisposeTask].attach(obj_.work_on)
        self.log(f"{obj_} queued for a task")
        return True

    def dispose_task(self, task: tasks.Task) -> bool:
        if self._events[EventNames.DisposeTask].empty:
            return False

        self._events[EventNames.DisposeTask](task)
        return True
