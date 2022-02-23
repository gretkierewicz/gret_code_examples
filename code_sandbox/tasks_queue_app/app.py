import enum
import time
from typing import Any, Dict, Iterable

from . import entities, tasks


class App:
    _event_pool: Dict[enum.Enum, Any]
    _task_pool: tasks.TaskPool

    _start_time: float

    def __init__(self) -> None:
        self._event_pool = entities.create_event_pool()
        self._task_pool = tasks.TaskPool()

        self._start_time = time.time()
        self._event_pool[entities.EntityEvents.Log].attach(self.print_msg)

    def run(self) -> None:
        self._event_pool[entities.EntityEvents.Update]()
        self._event_pool[entities.EntityEvents.AfterUpdate]()
        self._event_pool[entities.EntityEvents.DistributeTasks](self._task_pool)

    def add_entities(self, *entities_: entities.Entity) -> None:
        for entity in entities_:
            entity.subscribe(self._event_pool)

    def remove_entities(self, *entities_: entities.Entity) -> None:
        for entity in entities_:
            entity.unsubscribe()

    def load_tasks(self, tasks_iterable: Iterable[tasks.Task]) -> None:
        self._task_pool.put(*tasks_iterable)

    def print_msg(self, message: str) -> None:
        print(f"Time: {time.time() - self._start_time:.2f}s | {message}")
