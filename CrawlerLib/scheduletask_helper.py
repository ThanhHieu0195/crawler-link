import sched
import time
import datetime
from Background.masterclient import assign_task
from Configs import constant
from CrawlerLib.Pymongo import MongodbClient
from CrawlerLib.helper import get_utc_time, get_master_attr
from CrawlerLib.show_notify import show_warning, show_debug
import requests
import threading


client = MongodbClient.get_instance()


def job(data):
    assign_task(data)
    process_result_callback(data['link_id'])


def get_data_hook(link_id, link):
    link_type = get_master_attr('type', link, None)
    data = {
        'link_id': link_id,
        'user_id': get_master_attr('profile.id', link, None),
        'user_name': get_master_attr('profile.username', link, None),
        'user_display': get_master_attr('profile.display_name', link, None),
        'post_created_time': get_master_attr('post_created_time', link, None),
        'type': link_type,
        'screenshot': get_master_attr('screenshot', link, None)
    }

    if link_type == constant.TYPE_FB:
        data['reactions'] = get_master_attr('reactions', link, None)
        data['comments'] = get_master_attr('comments', link, None)
        data['shares'] = get_master_attr('shares', link, None)

    if link_type == constant.TYPE_INS:
        data['likes'] = get_master_attr('likes', link, None)
        data['comments'] = get_master_attr('comments', link, None)

    if link_type == constant.TYPE_YTB:
        data['views'] = get_master_attr('views', link, None)
        data['comments'] = get_master_attr('comments', link, None)
        data['likes'] = get_master_attr('likes', link, None)
        data['dislikes'] = get_master_attr('dislikes', link, None)

    return data


def process_result_callback(link_id):
    link = client.get_link_collection().find_one({"link_id": link_id})
    if not link:
        print('Not found link')
        return None
    hook_url = get_master_attr('hook_url', link, None)
    if hook_url:
        data = get_data_hook(link_id, link)
        try:
            requests.post(hook_url, data)
        except requests.exceptions.ConnectionError as e1:
            show_warning(format(e1))
        except Exception as e:
            show_warning(format(e))

        show_debug('Hook request %s' % link_id)
        print(data)


def start_schedule():
    year = int(get_utc_time('%Y'))
    month = int(get_utc_time('%m'))
    day = int(get_utc_time('%d'))
    condition = {
        "status": 1,
        "camp_start": {
            "$lte": datetime.datetime(year, month, day)
       },
        "deadline": {
            "$gte": datetime.datetime(year, month, day)
        },
        "timeline": '%s:00' % get_utc_time('%H')
    }

    show_debug('Execute schedule task ...')
    print(condition)
    data_tasks = client.get_link_collection().find(condition)

    s = sched.scheduler(time.time, time.sleep)

    tasks = list(data_tasks)
    data_crawler = []
    idx = 0
    for row in tasks:
        del row['_id']
        option = {
            'link_id': row['link_id'],
            'type': row['type']
        }
        data_crawler.append(option)
        idx += 1

    show_debug('%s task waiting exec' % len(data_crawler))


def process_list_job(arr):
    for j in arr:
        job(j)


def process_crawler_thread(data):
    x = threading.Thread(target=process_list_job, args=(data[0:int(len(data) / 2)],))
    y = threading.Thread(target=process_list_job, args=(data[int(len(data) / 2):len(data)],))
    x.start()
    y.start()

