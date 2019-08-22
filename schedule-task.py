import sched
import time
# from Background.masterclient import assign_task
from CrawlerLib.Pymongo import connect_mongo
client = connect_mongo()
data_tasks = client['crawler'].links.find()

def job(data):
    # assign_task(data)
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

