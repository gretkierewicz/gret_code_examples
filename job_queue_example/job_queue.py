import random
import time
from typing import List, Optional

import events


class App:
    def __init__(self) -> None:
        self._start_time = time.time()

        self.dispose_job_event: events.Event = events.Event(
            events.EventDistributionFactory.create_for_first_to_take
        )

        self.update_event: events.Event = events.Event()
        self.after_update_event: events.Event = events.Event()

        self.job_list = []

    @property
    def start_time(self) -> float:
        return self._start_time

    def run(self) -> None:
        self.update_event()
        self.after_update_event()


class Job:
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


class Worker:
    def __init__(self, app: App, name: str) -> None:
        self._app = app
        self._name = name
        self._current_job: Optional[Job] = None

        self._app.update_event.attach(self.update)
        self._app.after_update_event.attach(self.after_update)

    def __str__(self) -> str:
        return self.name

    @property
    def name(self) -> str:
        return self._name

    def update(self) -> None:
        if not self._current_job:
            self._queue_for_a_job()
            return

        if self._current_job.is_done:
            self._current_job = None

    def after_update(self) -> None:
        pass

    def _queue_for_a_job(self) -> None:
        if self._get_a_job in self._app.dispose_job_event:
            return

        print(
            f"Time: {time.time() - self._app.start_time:.2f}s | {self} queued for a job"
        )
        self._app.dispose_job_event.attach(self._get_a_job)

    def _get_a_job(self, job: Job) -> None:
        self._current_job = job
        self._current_job.start()
        print(
            f"Time: {time.time() - self._app.start_time:.2f}s | "
            f"{self} was managed to work over {job} "
            f"(estimated time: {job.estimated_time:.2f}s)"
        )


class Manager(Worker):
    def __init__(self, app: App, name: str) -> None:
        super().__init__(app, name)

        self._job_list: List[Job] = []
        self._jobs_queue_len = 1
        self._was_job_disposed = False

    @property
    def max_queued_jobs(self) -> int:
        """Maximum amount of jobs to collect. For no limit, set to 0"""
        return self._jobs_queue_len

    @max_queued_jobs.setter
    def max_queued_jobs(self, value: int) -> None:
        self._jobs_queue_len = max(0, int(value))

    def update(self) -> None:
        self._collect_job()
        self._dispose_job()

    def after_update(self) -> None:
        if not self._was_job_disposed:
            return

        # this assures that manager waits for another managers to dispose their jobs
        self._app.update_event.reattach(self.update)
        self._was_job_disposed = False
        print(
            f"Time: {time.time() - self._app.start_time:.2f}s | "
            f"{self} moved to the end of queue"
        )

    def _dispose_job(self) -> None:
        if not self._job_list:
            return

        if self._app.dispose_job_event.is_empty:
            return

        self._app.dispose_job_event(self._job_list[0])
        print(
            f"Time: {time.time() - self._app.start_time:.2f}s | "
            f"{self} disposed {self._job_list[0]} successfully"
        )
        self._job_list.pop(0)

    def _collect_job(self) -> None:
        if not self._app.job_list:
            return

        if self.max_queued_jobs and len(self._job_list) >= self.max_queued_jobs:
            return

        collected_job = self._app.job_list.pop()
        self._job_list.append(collected_job)
        print(
            f"Time: {time.time() - self._app.start_time:.2f}s | "
            f"{self} collected {collected_job} | jobs to dispose: "
            f"{[str(job) for job in self._job_list]}"
        )
