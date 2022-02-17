import time

from .events import Event, ForFirstToTakeDistribution


class App:
    def __init__(self) -> None:
        self._start_time = time.time()

        self.dispose_job_event: Event = Event()
        self.dispose_job_event.call_strategy = ForFirstToTakeDistribution()

        self.update_event: Event = Event()
        self.after_update_event: Event = Event()

        self.job_list = []

    def log(self, message) -> None:
        print(f"Time: {time.time() - self._start_time:.2f}s | {message}")

    def run(self) -> None:
        self.update_event()
        self.after_update_event()
