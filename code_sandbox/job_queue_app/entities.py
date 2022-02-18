from typing import List, Optional

from . import app, jobs


class Entity(app.IUpdatable):
    def __init__(self, app_: app.App, name: str) -> None:
        self._app = app_
        self._name = name

        self._app.subscribe(self)

    def __str__(self) -> str:
        return self.name

    @property
    def name(self) -> str:
        return self._name

    def update(self):
        pass

    def after_update(self):
        pass


class Worker(Entity, app.IWorkable):
    _current_job: Optional[jobs.Job]

    def __init__(self, app_: app.App, name: str) -> None:
        super().__init__(app_, name)
        self._current_job = None

    def update(self) -> None:
        if not self._current_job:
            self._queue_for_a_job()
            return

        if self._current_job.is_done:
            self._current_job = None

    def _queue_for_a_job(self) -> None:
        joined_job_disposition = self._app.join_job_disposition(self)
        if joined_job_disposition:
            self._app.log(f"{self} queued for a job")

    def run_a_job(self, job: jobs.Job) -> None:
        self._current_job = job
        self._current_job.start()
        self._app.log(
            f"{self} was managed to work over {job} "
            f"(estimated time: {job.estimated_time:.2f}s)"
        )


class Manager(Entity):
    _job_list: List[jobs.Job]
    _jobs_queue_len: int
    _disposed_job: bool

    def __init__(self, app_: app.App, name: str) -> None:
        super().__init__(app_, name)

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
        self._app.unsubscribe(self)
        self._app.subscribe(self)
        self._disposed_job = False
        self._app.log(f"{self} moved to the end of the queue")

    def _dispose_job(self) -> None:
        if not self._job_list:
            return

        job_disposed = self._app.dispose_job(self._job_list[0])
        if not job_disposed:
            return

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
