# Job queue example

---

### Idea

Using Event (list of callbacks) construct for creating simple app that
allows distribution of jobs.

---

### Sample output:

* Workers: 
    * Steve
    * Sophi
* Managers: 
    * Irene - list of jobs to dispose limit = 1
    * Clark - list of jobs to dispose limit = 2

```bash

Time: 0.00s | Steve (w) queued for a job
Time: 0.00s | Sophi (w) queued for a job

Time: 0.00s | Irene (M) collected Job nr 0 | jobs to dispose: ['Job nr 0']
Time: 0.00s | Steve (w) was managed to work over Job nr 0 (estimated time: 0.16s)
Time: 0.00s | Irene (M) disposed Job nr 0 successfully

Time: 0.00s | Clark (M) collected Job nr 1 | jobs to dispose: ['Job nr 1']
Time: 0.00s | Sophi (w) was managed to work over Job nr 1 (estimated time: 0.05s)
Time: 0.00s | Clark (M) disposed Job nr 1 successfully

Time: 0.00s | Irene (M) moved to the end of queue
Time: 0.00s | Clark (M) moved to the end of queue

Time: 0.00s | Irene (M) collected Job nr 2 | jobs to dispose: ['Job nr 2']
Time: 0.00s | Clark (M) collected Job nr 3 | jobs to dispose: ['Job nr 3']
Time: 0.00s | Clark (M) collected Job nr 4 | jobs to dispose: ['Job nr 3', 'Job nr 4']

Time: 0.05s | Sophi (w) queued for a job
Time: 0.05s | Sophi (w) was managed to work over Job nr 2 (estimated time: 0.11s)
Time: 0.05s | Irene (M) disposed Job nr 2 successfully
Time: 0.05s | Irene (M) moved to the end of queue

Time: 0.16s | Sophi (w) queued for a job
Time: 0.16s | Sophi (w) was managed to work over Job nr 3 (estimated time: 0.11s)
Time: 0.16s | Clark (M) disposed Job nr 3 successfully
Time: 0.16s | Clark (M) moved to the end of queue

Time: 0.16s | Steve (w) queued for a job
Time: 0.16s | Steve (w) was managed to work over Job nr 4 (estimated time: 0.20s)
Time: 0.16s | Clark (M) disposed Job nr 4 successfully
Time: 0.16s | Clark (M) moved to the end of queue

Time: 0.27s | Sophi (w) queued for a job
Time: 0.36s | Steve (w) queued for a job
```