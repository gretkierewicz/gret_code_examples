"""
Module for running example of tasks queue
"""
from . import app, entities, tasks

if __name__ == "__main__":
    main_app = app.App()
    main_app.load_tasks(tasks.Task(f"Task nr {i}") for i in range(5))

    w1 = entities.Worker("Steve (w)")
    w2 = entities.Worker("Sophi (w)")

    m1 = entities.Manager("Irene (M)")
    m2 = entities.Manager("Clark (M)")
    m2.max_queued_tasks = 2

    main_app.add_entities(w1, w2, m1, m2)

    while True:
        main_app.run()
