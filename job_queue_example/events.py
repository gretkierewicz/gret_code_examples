import abc
from typing import Callable, Iterator, List, Optional


class EventContainer(abc.ABC):
    _list: List[Callable]

    @abc.abstractmethod
    def __bool__(self) -> bool:
        pass

    @abc.abstractmethod
    def __contains__(self, item: Callable) -> bool:
        pass

    @abc.abstractmethod
    def __iter__(self) -> Iterator[Callable]:
        pass

    @abc.abstractmethod
    def pop(self, idx: Optional[int] = None) -> Callable:
        pass


class EventDistribution(abc.ABC):
    context: EventContainer

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


class EventDistributionFactory:
    @staticmethod
    def create_for_every_callback(context: EventContainer):
        strategy = ForEveryCallbackDistribution()
        strategy.set_context(context)
        return strategy

    @staticmethod
    def create_for_first_to_take(context: EventContainer):
        strategy = ForFirstToTakeDistribution()
        strategy.set_context(context)
        return strategy


class Event(EventContainer):
    _call_event_strategy: EventDistribution

    def __init__(
        self,
        create_strategy: Callable[
            [EventContainer], EventDistribution
        ] = EventDistributionFactory.create_for_every_callback,
    ) -> None:
        self._list = []

        self._call_event_strategy = create_strategy(self)

    # Start of abstract methods implementation ------------------------------------------

    def __bool__(self) -> bool:
        return True if self._list else False

    def __contains__(self, item: Callable) -> bool:
        return item in self._list

    def __iter__(self) -> Iterator[Callable]:
        return self._list.__iter__()

    def pop(self, idx: Optional[int] = None) -> Callable:
        if idx is None:
            idx = -1

        return self._list.pop(idx)

    # End of abstract methods implementation --------------------------------------------

    def __call__(self, *args, **kwargs) -> bool:
        return self._call_event_strategy.call_event(*args, **kwargs)

    @property
    def is_empty(self) -> bool:
        return not self

    def attach(self, func: Callable) -> None:
        if func not in self._list:
            self._list.append(func)

    def detach(self, func: Callable = None) -> None:
        if func in self._list:
            self._list.remove(func)

    def reattach(self, func: Callable) -> None:
        self.detach(func)
        self.attach(func)
