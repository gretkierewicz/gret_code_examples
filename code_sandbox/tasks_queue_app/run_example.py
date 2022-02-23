"""
Module for running example of tasks queue
"""
import random

from . import app

random.seed(321322)

if __name__ == "__main__":
    task_list = [app.src.Task(f"Task nr {i}") for i in range(5)]
    for task in task_list:
        task.seconds_to_finish = random.uniform(0.02, 0.2)

    main_app = app.App()
    main_app.load_tasks(task_list)

    w1 = app.src.Worker("Steve (w)")
    w2 = app.src.Worker("Sophi (w)")

    m1 = app.src.Manager("Irene (M)")
    m2 = app.src.Manager("Clark (M)")
    m1.max_queued_tasks = 2

    main_app.add_entities(w1, w2, m1, m2)

    while True:
        main_app.run()
