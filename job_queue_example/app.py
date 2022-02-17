import time

from .events import Event, EventDistributionFactory


class App:
    def __init__(self) -> None:
        self._start_time = time.time()

        self.dispose_job_event: Event = Event(
            EventDistributionFactory.create_for_first_to_take
        )

        self.update_event: Event = Event()
        self.after_update_event: Event = Event()

        self.job_list = []

    @property
    def start_time(self) -> float:
        return self._start_time

    def run(self) -> None:
        self.update_event()
        self.after_update_event()
