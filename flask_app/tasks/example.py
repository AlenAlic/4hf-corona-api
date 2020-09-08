import time
from rq import get_current_job


def count_up(seconds):
    job = get_current_job()
    print("Starting task")
    for i in range(seconds):
        job.meta["progress"] = 100.0 * i / seconds
        job.save_meta()
        print(f"{int(job.meta['progress'])}%")
        time.sleep(0.25)
    job.meta["progress"] = 100
    job.save_meta()
    print("Task completed")
