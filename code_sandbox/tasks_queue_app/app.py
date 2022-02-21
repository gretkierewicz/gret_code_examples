import time
from typing import Any, Iterable, List, Optional, Protocol

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


class App:
    _update_event: utils.Event
    _after_update_event: utils.Event

    _dispose_task_event: utils.Event

    _tasks_pool: List[tasks.Task]
    _start_time: float

    def __init__(self) -> None:
        self._start_time = time.time()

        self._update_event = utils.Event()
        self._after_update_event = utils.Event()

        self._dispose_task_event = utils.Event()
        self._dispose_task_event.event_distribution = utils.ForFirstToTakeDistribution()

        self._tasks_pool = []

    def log(self, message: Any) -> None:
        print(f"Time: {time.time() - self._start_time:.2f}s | {message}")

    def run(self) -> None:
        self._update_event()
        self._after_update_event()

    def subscribe(self, obj_: SupportsUpdates) -> None:
        self._update_event.attach(obj_.update)
        self._after_update_event.attach(obj_.after_update)

    def unsubscribe(self, obj_: SupportsUpdates) -> None:
        self._update_event.detach(obj_.update)
        self._after_update_event.detach(obj_.after_update)

    def load_tasks(self, tasks_iterable: Iterable[tasks.Task]) -> None:
        self._tasks_pool += list(tasks_iterable)

    def get_task(self) -> Optional[tasks.Task]:
        if not self._tasks_pool:
            return None

        return self._tasks_pool.pop()

    def join_task_disposition(self, obj_: SupportsWorking) -> bool:
        if obj_.work_on in self._dispose_task_event:
            return False

        self._dispose_task_event.attach(obj_.work_on)
        self.log(f"{obj_} queued for a task")
        return True

    def dispose_task(self, task: tasks.Task) -> bool:
        if self._dispose_task_event.empty:
            return False

        self._dispose_task_event(task)
        return True
