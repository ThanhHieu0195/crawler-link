from CrawlerLib.Pymongo import MongodbClient
from Background.masterclient import assign_task
from Configs import constant
import threading
import datetime

from CrawlerLib.helper import get_utc_time

link_social = [
    {'link_id': 'OLEDJGtxDLs', 'type': constant.TYPE_YTB},
    {'link_id': 'IyhSUdLEh9g', 'type': constant.TYPE_YTB},
    {'link_id': '12FDmPuAr4I', 'type': constant.TYPE_YTB},
    {'link_id': '3QM0SPSjMFI', 'type': constant.TYPE_YTB},
    {'link_id': 'q1aqSgiFvyU', 'type': constant.TYPE_YTB},
    {'link_id': '1WJm3WvZHM8', 'type': constant.TYPE_YTB},

    {'link_id': 'B2E49_MA_x7', 'type': constant.TYPE_INS},
    {'link_id': 'B1pidq3gKow', 'type': constant.TYPE_INS},
    {'link_id': 'BqkRJwMFtMb', 'type': constant.TYPE_INS},
    {'link_id': 'BiLgoGSg9I5', 'type': constant.TYPE_INS},
    {'link_id': 'BfhpgMXApid', 'type': constant.TYPE_INS},

    {'link_id': '100003880005704_1465875616885091', 'type': constant.TYPE_FB},
    {'link_id': '911595358960653_2510103575776482', 'type': constant.TYPE_FB},
    {'link_id': '100004841792517_1186286404876075', 'type': constant.TYPE_FB},
    {'link_id': '100009774090489_907659462903182', 'type': constant.TYPE_FB},
]


def job(data):
    assign_task(data)


def init_data(arr):
    for data in arr:
        data['timeline'] = '00:00'
        data['camp_start'] = datetime.datetime.now()
        data['deadline'] = datetime.datetime.now()
        MongodbClient.get_instance().get_link_collection().insert(data)


def process_list_job(arr):
    for j in arr:
        job(j)


def process_jobs():
    print('Total link: ', len(link_social))
    x = threading.Thread(target=process_list_job, args=(link_social[0:int(len(link_social) / 2)],))
    y = threading.Thread(target=process_list_job, args=(link_social[int(len(link_social) / 2):len(link_social)],))
    x.start()
    y.start()


# init_data(link_social)
process_jobs()
