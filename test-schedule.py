import sched
import time
from Background.masterclient import assign_task
from CrawlerLib.Pymongo import MongodbClient
import pprint


client = MongodbClient.get_instance()
data_tasks = client.get_link_collection().find()


def job(data):
    assign_task(data)


# job({
#     'link_id': 'j8U06veqxdU',
#     'type': 'YT'
# })
# if data_tasks.count() > 0:
#     for i in range(0, data_tasks.count()):
#         o=data_tasks[i]
#         job({
#             'link_id': o['link_id'],
#             'type': o['type']
#         })

# job({'type': 'YT', 'link_id': 'j8U06veqxdU'})
# job({'type': 'IG', 'link_id': 'BqkRJwMFtMb'})
# job({'type': 'IG', 'link_id': 'BqkRJwMFtMb'})
# job({'type': 'IG', 'link_id': 'BqkRJwMFtMb'})
# job({'type': 'IG', 'link_id': 'BqkRJwMFtMb'})
# job({'type': 'IG', 'link_id': 'BqkRJwMFtMb'})
# job({'type': 'IG', 'link_id': 'BcNyJJLAGOe'})
# job({'type': 'YT', 'link_id': 'j8U06veqxdU'})
# job({'type': 'YT', 'link_id': 'j8U06veqxdU'})
job({'type': 'YT', 'link_id': '0RH0Xf3Iw5g'})

# job({'type': 'FB', 'link_id': '100003803082906_1486305034839585'})
