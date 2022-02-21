# Task queue app

---
### Assumptions

- Using Event (list of callbacks) construct for creating simple app that
allows distribution of tasks.

---
### Example of output:

* Workers: 
    * Steve
    * Sophi
- Managers: 
    * Irene - list of tasks to dispose limit = 1
    * Clark - list of tasks to dispose limit = 2

```bash
Time: 0.00s | Steve (w) queued for a task
Time: 0.00s | Sophi (w) queued for a task

Time: 0.00s | Irene (M) collected Task nr 0 | tasks to dispose: ['Task nr 0']
Time: 0.00s | Sophi (w) was managed to work over Task nr 0 (estimated time: 0.15s)
Time: 0.00s | Irene (M) disposed Task nr 0 successfully

Time: 0.00s | Clark (M) collected Task nr 1 | tasks to dispose: ['Task nr 1']
Time: 0.00s | Steve (w) was managed to work over Task nr 1 (estimated time: 0.13s)
Time: 0.00s | Clark (M) disposed Task nr 1 successfully

Time: 0.00s | Irene (M) moved to the end of the queue
Time: 0.00s | Clark (M) moved to the end of the queue

Time: 0.00s | Irene (M) collected Task nr 2 | tasks to dispose: ['Task nr 2']
Time: 0.00s | Clark (M) collected Task nr 3 | tasks to dispose: ['Task nr 3']
Time: 0.00s | Clark (M) collected Task nr 4 | tasks to dispose: ['Task nr 3', 'Task nr 4']

Time: 0.13s | Steve (w) queued for a task
Time: 0.13s | Steve (w) was managed to work over Task nr 2 (estimated time: 0.06s)
Time: 0.13s | Irene (M) disposed Task nr 2 successfully
Time: 0.13s | Irene (M) moved to the end of the queue

Time: 0.15s | Sophi (w) queued for a task
Time: 0.15s | Sophi (w) was managed to work over Task nr 3 (estimated time: 0.07s)
Time: 0.15s | Clark (M) disposed Task nr 3 successfully
Time: 0.15s | Clark (M) moved to the end of the queue

Time: 0.19s | Steve (w) queued for a task
Time: 0.19s | Steve (w) was managed to work over Task nr 4 (estimated time: 0.05s)
Time: 0.19s | Clark (M) disposed Task nr 4 successfully
Time: 0.19s | Clark (M) moved to the end of the queue

Time: 0.22s | Sophi (w) queued for a task
Time: 0.24s | Steve (w) queued for a task
```

---