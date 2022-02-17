import abc
from typing import List, Optional

from .app import App
from .jobs import Job


class Entity(abc.ABC):
    def __init__(self, app: App, name: str) -> None:
        self._app = app
        self._name = name

        self._app.update_event.attach(self.update)
        self._app.after_update_event.attach(self.after_update)

    def __str__(self) -> str:
        return self.name

    @property
    def name(self) -> str:
        return self._name

    @abc.abstractmethod
    def update(self):
        pass

    def after_update(self):
        pass


class Worker(Entity):
    _current_job: Optional[Job]

    def __init__(self, app: App, name: str) -> None:
        super().__init__(app, name)
        self._current_job = None

    def update(self) -> None:
        if not self._current_job:
            self._queue_for_a_job()
            return

        if self._current_job.is_done:
            self._current_job = None

    def _queue_for_a_job(self) -> None:
        if self._get_a_job in self._app.dispose_job_event:
            return

        self._app.dispose_job_event.attach(self._get_a_job)
        self._app.log(f"{self} queued for a job")

    def _get_a_job(self, job: Job) -> None:
        self._current_job = job
        self._current_job.start()
        self._app.log(
            f"{self} was managed to work over {job} "
            f"(estimated time: {job.estimated_time:.2f}s)"
        )


class Manager(Entity):
    _job_list: List[Job]
    _jobs_queue_len: int
    _disposed_job: bool

    def __init__(self, app: App, name: str) -> None:
        super().__init__(app, name)

        self._job_list = []
        self._jobs_queue_len = 1
        self._disposed_job = False

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
        if not self._disposed_job:
            return

        # this assures that manager waits for another managers to dispose their jobs
        self._app.update_event.reattach(self.update)
        self._disposed_job = False
        self._app.log(f"{self} moved to the end of the queue")

    def _dispose_job(self) -> None:
        if not self._job_list:
            return

        if not self._app.dispose_job_event:
            return

        self._app.dispose_job_event(self._job_list[0])
        self._app.log(f"{self} disposed {self._job_list[0]} successfully")
        self._disposed_job = True
        self._job_list.pop(0)

    def _collect_job(self) -> None:
        if not self._app.job_list:
            return

        if self.max_queued_jobs and len(self._job_list) >= self.max_queued_jobs:
            return

        collected_job = self._app.job_list.pop()
        self._job_list.append(collected_job)
        self._app.log(
            f"{self} collected {collected_job} | jobs to dispose: "
            f"{[str(job) for job in self._job_list]}"
        )
