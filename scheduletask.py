import sched
import time
import datetime
from Background.masterclient import assign_task
from CrawlerLib.Pymongo import MongodbClient
from CrawlerLib.show_notify import show_text


print("=========================================")
print("Today: " + time.strftime('%d-%m-%Y %H:%M', time.gmtime()))


def job(data):
    assign_task(data)


client = MongodbClient.get_instance()

year = int(time.strftime('%Y', time.gmtime()))
month = int(time.strftime('%m', time.gmtime()))
day = int(time.strftime('%y', time.gmtime()))
hour = int(time.strftime('%H', time.gmtime()))


condition = {
    "status": 1,
    "deadline": {
        "$gt": datetime.datetime(year, month, day)
    },
    "timeline": '%s:00' % hour
}

show_text('Execute scheduletask ...')
print(condition)
data_tasks = client.get_link_collection().find(condition)

s = sched.scheduler(time.time, time.sleep)

tasks = list(data_tasks)
idx=0
for row in tasks:
    del row['_id']
    option = {
        'link_id': row['link_id'],
        'type': row['type']
    }
    s.enter(idx * 10, 1, job, (option,))
    idx += 1

print('%s task waiting exec' % len(tasks))
s.run()
print('DONE')
