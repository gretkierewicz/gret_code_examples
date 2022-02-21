from typing import List, Optional

from . import app, tasks


class Entity(app.SupportsUpdates):
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


class Worker(Entity, app.SupportsWorking):
    _current_task: Optional[tasks.Task]

    def __init__(self, app_: app.App, name: str) -> None:
        super().__init__(app_, name)
        self._current_task = None

    def update(self) -> None:
        if not self._current_task:
            self._queue_for_a_task()
            return

        if self._current_task.is_done:
            self._current_task = None

    def _queue_for_a_task(self) -> None:
        joined_task_disposition = self._app.join_task_disposition(self)
        if joined_task_disposition:
            self._app.log(f"{self} queued for a task")

    def work_on(self, task: tasks.Task) -> None:
        self._current_task = task
        self._current_task.start()
        self._app.log(
            f"{self} was managed to work over {task} "
            f"(estimated time: {task.estimated_time:.2f}s)"
        )


class Manager(Entity):
    _tasks_pool: List[tasks.Task]
    _tasks_queue_len: int
    _disposed_task: bool

    def __init__(self, app_: app.App, name: str) -> None:
        super().__init__(app_, name)

        self._tasks_pool = []
        self._tasks_queue_len = 1
        self._disposed_task = False

    @property
    def max_queued_tasks(self) -> int:
        """Maximum amount of tasks to collect. For no limit, set to 0"""
        return self._tasks_queue_len

    @max_queued_tasks.setter
    def max_queued_tasks(self, value: int) -> None:
        self._tasks_queue_len = max(0, int(value))

    def update(self) -> None:
        self._collect_task()
        self._dispose_task()

    def after_update(self) -> None:
        if not self._disposed_task:
            return

        # this assures that manager waits for another managers to dispose their tasks
        self._app.unsubscribe(self)
        self._app.subscribe(self)
        self._disposed_task = False
        self._app.log(f"{self} moved to the end of the queue")

    def _dispose_task(self) -> None:
        if not self._tasks_pool:
            return

        task_disposed = self._app.dispose_task(self._tasks_pool[0])
        if not task_disposed:
            return

        self._app.log(f"{self} disposed {self._tasks_pool[0]} successfully")
        self._disposed_task = True
        self._tasks_pool.pop(0)

    def _collect_task(self) -> None:
        if not self._app.tasks_list:
            return

        if self.max_queued_tasks and len(self._tasks_pool) >= self.max_queued_tasks:
            return

        collected_task = self._app.tasks_list.pop()
        self._tasks_pool.append(collected_task)
        self._app.log(
            f"{self} collected {collected_task} | tasks to dispose: "
            f"{[str(task) for task in self._tasks_pool]}"
        )
