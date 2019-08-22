import sched
import time
from masterclient import assign_task

data_tasks = [
    {
        "id": "100003803082906_1509228895880532",
        "type": "fb",
        "loop": ['16:41']
    },
    {
        "id": "BqkRJwMFtMb",
        "type": "ins",
        "loop": ['16:42']
    }
]


def job(data):
    assign_task(data)
    print(data)

hours = int(time.strftime('%H'))
minus = int(time.strftime('%M'))
time_current = hours * 60 + minus

s = sched.scheduler(time.time, time.sleep)

for row in data_tasks:
    for loop in row['loop']:
        h, i = loop.split(':')
        time_job = int(h) * 60 + int(i)
        rg_time = time_job - time_current
        if rg_time >= 0:
            s.enter(rg_time * 60, 1, job, (row, ))

s.run()

