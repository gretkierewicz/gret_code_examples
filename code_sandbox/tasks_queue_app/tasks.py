import time
from typing import Iterator, List, Optional


class Task:
    def __init__(self, name: str) -> None:
        self._name = name
        self._seconds_to_finish = 0
        self._start_time = None

    def __str__(self) -> str:
        return self.name

    @property
    def name(self) -> str:
        return self._name

    @property
    def seconds_to_finish(self) -> float:
        return self._seconds_to_finish

    @seconds_to_finish.setter
    def seconds_to_finish(self, seconds: float) -> None:
        self._seconds_to_finish = max(.0, seconds)

    @property
    def is_done(self) -> bool:
        return time.time() - self._start_time >= self.seconds_to_finish

    def start(self) -> None:
        self._start_time = time.time()


class TaskPool:
    _pool: List[Task]

    def __init__(self):
        self._pool = []

    def put(self, *tasks: Task) -> None:
        self._pool += list(tasks)

    def get(self) -> Optional[Task]:
        if not self._pool:
            return None

        return self._pool.pop(0)

    def __iter__(self) -> Iterator[Task]:
        return self._pool.__iter__()

    def __len__(self):
        return len(self._pool)
