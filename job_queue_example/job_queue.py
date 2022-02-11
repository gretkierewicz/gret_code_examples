import random
from time import time
from typing import Callable, List, Optional


class Event:
    def __init__(self) -> None:
        self._list: List[Callable] = []

    def __call__(self, *args, **kwargs) -> None:
        for item in self._list:
            item(*args, **kwargs)

    def __contains__(self, item) -> bool:
        return item in self._list

    def attach(self, func: Callable) -> None:
        if func not in self._list:
            self._list.append(func)

    def detach(self, func: Callable) -> None:
        if func in self._list:
            self._list.remove(func)

    def move_to_end_of_queue(self, func: Callable) -> None:
        if func in self._list:
            self.detach(func)
        self.attach(func)


class JobQueue(Event):
    def __call__(self, *args, **kwargs) -> bool:
        if not self._list:
            return False
        item = self._list.pop(0)  # 0 so first observer subscribed is taken first
        item(*args, **kwargs)
        return True


class App:
    def __init__(self) -> None:
        self._start_time = time()

        self.dispose_job_event = JobQueue()

        self.update_event = Event()
        self.after_update_event = Event()

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
        return time() - self._start_time >= self.estimated_time

    def start(self) -> None:
        self._start_time = time()


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
        if self._current_job and self._current_job.is_done:
            self._current_job = None

        self._queue_for_a_job()

    def after_update(self) -> None:
        pass

    def _queue_for_a_job(self) -> None:
        if self._current_job:
            return
        if self._get_a_job in self._app.dispose_job_event:
            return

        print(f"Time: {time() - self._app.start_time:.2f}s | {self} queued for a job")
        self._app.dispose_job_event.attach(self._get_a_job)

    def _get_a_job(self, job: Job) -> None:
        self._current_job = job
        self._current_job.start()
        print(
            f"Time: {time() - self._app.start_time:.2f}s | "
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
    def jobs_queue_len(self) -> int:
        """Maximum amount of jobs to collect. For no limit, set to 0"""
        return self._jobs_queue_len

    @jobs_queue_len.setter
    def jobs_queue_len(self, value: int) -> None:
        self._jobs_queue_len = max(0, int(value))

    def update(self) -> None:
        self._collect_job()
        self._dispose_job()

    def after_update(self) -> None:
        if not self._was_job_disposed:
            return

        # this assures that manager waits for another managers to dispose their jobs
        self._app.update_event.move_to_end_of_queue(self.update)
        self._was_job_disposed = False
        print(
            f"Time: {time() - self._app.start_time:.2f}s | "
            f"{self} moved to the end of queue"
        )

    def _dispose_job(self) -> None:
        if not self._job_list:
            return

        self._was_job_disposed: bool = self._app.dispose_job_event(self._job_list[0])
        if self._was_job_disposed:
            print(
                f"Time: {time() - self._app.start_time:.2f}s | "
                f"{self} disposed {self._job_list[0]} successfully"
            )
            self._job_list.pop(0)

    def _collect_job(self) -> None:
        if not self._app.job_list:
            return

        if self.jobs_queue_len and len(self._job_list) >= self.jobs_queue_len:
            return

        collected_job = self._app.job_list.pop()
        self._job_list.append(collected_job)
        print(
            f"Time: {time() - self._app.start_time:.2f}s | "
            f"{self} collected {collected_job} | jobs to dispose: "
            f"{[str(job) for job in self._job_list]}"
        )
