"""
Module for running example of tasks queue
"""
from . import app, entities, tasks

if __name__ == "__main__":
    main_app = app.App()
    main_app.load_tasks(tasks.Task(f"Task nr {i}") for i in range(5)[::-1])

    w1 = entities.Worker(main_app, "Steve (w)")
    w2 = entities.Worker(main_app, "Sophi (w)")

    m1 = entities.Manager(main_app, "Irene (M)")
    m2 = entities.Manager(main_app, "Clark (M)")
    m2.max_queued_tasks = 2

    while True:
        main_app.run()
