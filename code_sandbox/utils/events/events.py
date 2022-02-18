import abc
from typing import Callable, Iterator, List, Optional


__all__ = [
    "Event",
    "ForEveryCallbackDistribution",
    "ForFirstToTakeDistribution",
]


class EventDistribution(abc.ABC):
    context: "Event"

    def set_context(self, context):
        self.context = context

    @abc.abstractmethod
    def call_event(self, *args, **kwargs) -> bool:
        pass


class ForEveryCallbackDistribution(EventDistribution):
    def call_event(self, *args, **kwargs):
        for item in self.context:
            item(*args, **kwargs)
        else:
            return True


class ForFirstToTakeDistribution(EventDistribution):
    def call_event(self, *args, **kwargs) -> bool:
        if not self.context:
            return False

        item = self.context.pop()
        item(*args, **kwargs)
        return True


class Event:
    _list: List[Callable]
    _event_distribution: EventDistribution

    def __init__(self) -> None:
        self._list = []
        self.event_distribution = ForEveryCallbackDistribution()

    def __bool__(self) -> bool:
        return True if self._list else False

    def __call__(self, *args, **kwargs) -> bool:
        return self._event_distribution.call_event(*args, **kwargs)

    def __contains__(self, item: Callable) -> bool:
        return item in self._list

    def __iter__(self) -> Iterator[Callable]:
        return self._list.__iter__()

    @property
    def empty(self) -> bool:
        return not self

    @property
    def event_distribution(self) -> EventDistribution:
        return self._event_distribution

    @event_distribution.setter
    def event_distribution(self, event_distribution: EventDistribution) -> None:
        self._event_distribution = event_distribution
        self._event_distribution.set_context(self)

    def pop(self, idx: Optional[int] = None) -> Callable:
        if idx is None:
            idx = -1

        return self._list.pop(idx)

    def attach(self, func: Callable) -> None:
        if func not in self._list:
            self._list.append(func)

    def detach(self, func: Callable = None) -> None:
        if func in self._list:
            self._list.remove(func)

    def reattach(self, func: Callable) -> None:
        self.detach(func)
        self.attach(func)
