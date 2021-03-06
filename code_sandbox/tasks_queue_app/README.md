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
Time: 0.00s | Steve (w) queued for next task
Time: 0.00s | Sophi (w) queued for next task

Time: 0.00s | Irene (M) collected Task nr 0 | tasks to dispose: ['Task nr 0']
Time: 0.00s | Clark (M) collected Task nr 1 | tasks to dispose: ['Task nr 1']

Time: 0.00s | Sophi (w) starts working on Task nr 0 (est. time: 0.19s)
Time: 0.00s | Irene (M) disposed Task nr 0 successfully

Time: 0.00s | Steve (w) starts working on Task nr 1 (est. time: 0.12s)
Time: 0.00s | Clark (M) disposed Task nr 1 successfully

Time: 0.00s | Irene (M) moved to the end of the Update Event queue
Time: 0.00s | Clark (M) moved to the end of the Update Event queue

Time: 0.00s | Irene (M) collected Task nr 2 | tasks to dispose: ['Task nr 2']
Time: 0.00s | Clark (M) collected Task nr 3 | tasks to dispose: ['Task nr 3']
Time: 0.00s | Irene (M) collected Task nr 4 | tasks to dispose: ['Task nr 2', 'Task nr 4']

Time: 0.13s | Steve (w) done Task nr 1 and queued for next task
Time: 0.13s | Steve (w) starts working on Task nr 2 (est. time: 0.08s)
Time: 0.13s | Irene (M) disposed Task nr 2 successfully
Time: 0.13s | Irene (M) moved to the end of the Update Event queue

Time: 0.19s | Sophi (w) done Task nr 0 and queued for next task
Time: 0.19s | Sophi (w) starts working on Task nr 3 (est. time: 0.19s)
Time: 0.19s | Clark (M) disposed Task nr 3 successfully
Time: 0.19s | Clark (M) moved to the end of the Update Event queue

Time: 0.22s | Steve (w) done Task nr 2 and queued for next task
Time: 0.22s | Steve (w) starts working on Task nr 4 (est. time: 0.17s)
Time: 0.22s | Irene (M) disposed Task nr 4 successfully
Time: 0.22s | Irene (M) moved to the end of the Update Event queue

Time: 0.39s | Steve (w) done Task nr 4 and queued for next task
Time: 0.39s | Sophi (w) done Task nr 3 and queued for next task
```

---