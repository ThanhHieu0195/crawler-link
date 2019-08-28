import sched
import time
import datetime
from Background.masterclient import assign_task
from CrawlerLib.Pymongo import MongodbClient
from CrawlerLib.helper import get_utc_time, get_master_attr
from CrawlerLib.show_notify import show_text
import requests


client = MongodbClient.get_instance()


def job(data):
    assign_task(data)
    process_result_callback(data['link_id'])


def process_result_callback(link_id):
    link = client.get_link_collection().find_one({"link_id": link_id})
    hook_url = get_master_attr('hook_url', link, None)
    if hook_url:
        data = {
            'link_id': link_id,
            'user_id': get_master_attr('user_id', link, None),
            'comment': get_master_attr('comments', link, None),
            'shares': get_master_attr('shares', link, None),
            'reactions': get_master_attr('reactions', link, None),
            'views': get_master_attr('views', link, None),
            'post_created_time': get_master_attr('post_created_time', link, None),
            'type': get_master_attr('type', link, None),
        }
        requests.post(hook_url, data)
        show_text('Hook request %s' % link_id)
        print(data)


def start_schedule():
    year = int(get_utc_time('%Y'))
    month = int(get_utc_time('%m'))
    day = int(get_utc_time('%y'))
    hour = int(get_utc_time('%H'))

    condition = {
        "status": 1,
        "deadline": {
            "$gt": datetime.datetime(year, month, day)
        },
        "timeline": '%s:00' % hour
    }

    show_text('Execute schedule task ...')
    print(condition)
    data_tasks = client.get_link_collection().find(condition)

    s = sched.scheduler(time.time, time.sleep)

    tasks = list(data_tasks)
    idx = 0
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
