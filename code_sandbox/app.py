import abc
import time

from .events import Event, ForFirstToTakeDistribution
from .jobs import Job


class IUpdatable(abc.ABC):
    @abc.abstractmethod
    def update(self):
        pass

    @abc.abstractmethod
    def after_update(self):
        pass


class IWorkable(abc.ABC):
    @abc.abstractmethod
    def run_a_job(self, job: Job) -> None:
        pass


class App:
    def __init__(self) -> None:
        self._start_time = time.time()

        self._dispose_job_event: Event = Event()
        self._dispose_job_event.call_strategy = ForFirstToTakeDistribution()

        self._update_event: Event = Event()
        self._after_update_event: Event = Event()

        self.job_list = []

    def log(self, message) -> None:
        print(f"Time: {time.time() - self._start_time:.2f}s | {message}")

    def run(self) -> None:
        self._update_event()
        self._after_update_event()

    def subscribe(self, updatable: IUpdatable) -> None:
        self._update_event.attach(updatable.update)
        self._after_update_event.attach(updatable.after_update)

    def unsubscribe(self, updatable: IUpdatable) -> None:
        self._update_event.detach(updatable.update)
        self._after_update_event.detach(updatable.after_update)

    def join_job_disposition(self, worker: IWorkable) -> bool:
        if worker.run_a_job in self._dispose_job_event:
            return False
        self._dispose_job_event.attach(worker.run_a_job)
        return True

    def dispose_job(self, job: Job) -> bool:
        if not self._dispose_job_event:
            return False

        self._dispose_job_event(job)
        return True
