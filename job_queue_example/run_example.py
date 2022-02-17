"""
Module for running example of job queue
"""
from .app import App
from .entities import Manager, Worker
from .jobs import Job

if __name__ == "__main__":
    main_app = App()

    w1 = Worker(main_app, "Steve (w)")
    w2 = Worker(main_app, "Sophi (w)")

    main_app.job_list = [Job(f"Job nr {i}") for i in range(5)[::-1]]

    m1 = Manager(main_app, "Irene (M)")
    m2 = Manager(main_app, "Clark (M)")
    m2.max_queued_jobs = 2

    while True:
        main_app.run()
