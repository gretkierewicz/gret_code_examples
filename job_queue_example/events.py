import abc
from typing import Callable, List


class Event(abc.ABC):
    def __init__(self) -> None:
        self._list: List[Callable] = []

    @abc.abstractmethod
    def __call__(self, *args, **kwargs) -> bool:
        pass

    def __contains__(self, item) -> bool:
        return item in self._list

    def attach(self, func: Callable) -> None:
        if func not in self._list:
            self._list.append(func)

    def detach(self, func: Callable) -> None:
        if func in self._list:
            self._list.remove(func)

    def reattach(self, func: Callable) -> None:
        self.detach(func)
        self.attach(func)

    @property
    def is_empty(self) -> bool:
        return False if self._list else True


class EventForAll(Event):
    def __call__(self, *args, **kwargs) -> bool:
        for item in self._list:
            item(*args, **kwargs)
        else:
            return True


class EventForFirstToTake(EventForAll):
    def __call__(self, *args, **kwargs) -> bool:
        if not self._list:
            return False

        item = self._list.pop(0)
        item(*args, **kwargs)
        return True
