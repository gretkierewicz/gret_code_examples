import random
import time


class Task:
    def __init__(self, name: str) -> None:
        self._name = name
        self._estimated_time = random.uniform(0.02, 0.2)
        self._start_time = None

    def __str__(self) -> str:
        return self.name

    @property
    def name(self) -> str:
        return self._name

    @property
    def estimated_time(self) -> float:
        return self._estimated_time

    @property
    def is_done(self) -> bool:
        return time.time() - self._start_time >= self.estimated_time

    def start(self) -> None:
        self._start_time = time.time()
