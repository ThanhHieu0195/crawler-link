from Background.masterclient import assign_task
from Configs import constant
from CrawlerLib.Pymongo import MongodbClient
import datetime
import threading
from CrawlerLib.helper import get_utc_time
import time

client = MongodbClient.get_instance()
data_tasks = client.get_link_collection().find()


def job(data):
    assign_task(data)


link_ytb = [
    'OLEDJGtxDLs',
    'IyhSUdLEh9g',
    'LLlQsn52Dkc',
    # '12FDmPuAr4I',
    # '3QM0SPSjMFI',
    # 'xi1wK-aETw0',
    # 'q1aqSgiFvyU',
    # '1WJm3WvZHM8'
]


def init_data_ytb():
    for link_id in link_ytb:
        link_type = constant.TYPE_YTB
        data = {
            "hook_url": "http://dev.api.callback/callback-api/",
            "deadline": datetime.datetime.utcnow(),
            "status": 1,
            "timeline": [
                get_utc_time('%H') + ':00'
            ],
            "type": link_type,
            "camp_start": datetime.datetime.utcnow(),
            "link_id": link_id,
        }
        MongodbClient.get_instance().get_link_collection().insert(data)


def process_list_job(arr):
    for j in arr:
        job(j)


def process_jobs():
    list_a = []
    list_b = []

    for link_id in link_ytb[0:int(len(link_ytb) / 2)]:
        list_a.append({
            'link_id': link_id,
            'type': constant.TYPE_YTB
        })

    for link_id in link_ytb[int(len(link_ytb) / 2):len(link_ytb)]:
        list_b.append({
            'link_id': link_id,
            'type': constant.TYPE_YTB
        })

    x = threading.Thread(target=process_list_job, args=(list_a,))
    y = threading.Thread(target=process_list_job, args=(list_b,))
    x.start()
    y.start()


# init_data_ytb()
process_jobs()