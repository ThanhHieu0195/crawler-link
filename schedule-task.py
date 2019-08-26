import sched
import time
from Background.masterclient import assign_task
from CrawlerLib.Pymongo import MongodbClient


client = MongodbClient.get_instance()
data_tasks = client.get_link_collection().find()

def job(data):
    assign_task(data)


# hours = int(time.strftime('%H'))
# minus = int(time.strftime('%M'))
# time_current = hours * 60 + minus
#
# s = sched.scheduler(time.time, time.sleep)
#
# for row in data_tasks:
#     del row['_id']
#     for loop in row['loop']:
#         h, i = loop.split(':')
#         time_job = int(h) * 60 + int(i)
#         rg_time = time_job - time_current
#         if rg_time >= 0:
#             option = {
#                 'link_id': row['link_id'],
#                 'type': row['type']
#             }
#             s.enter(rg_time * 60, 1, job, (option, ))
#             print('task will exec at: ', loop)
#
# s.run()

job({
    'link_id': 'j8U06veqxdU',
    'type': 'ytb'
})
