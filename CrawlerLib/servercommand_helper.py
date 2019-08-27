import re
import time
from CrawlerLib.Pymongo import MongodbClient
from CrawlerLib.helper import get_master_attr
from CrawlerLib.show_notify import show_debug
import datetime
import pymongo


def detect_json(json_text):
    matches = re.findall(r'{(.*)}', json_text, re.DOTALL)
    if matches:
        return '{%s}' % matches[0]
    return None


def process_save_data_link(data):
    mongodb = MongodbClient.get_instance()
    link_collection = mongodb.get_link_collection()

    items = get_master_attr('body', data, [])
    hook_url = get_master_attr('hook_url', data, None)
    arr=[]
    for item in items:
        item['created_at'] = datetime.datetime.utcnow()
        item['updated_at'] = datetime.datetime.utcnow()
        item['status'] = 1
        item['hook_url'] = hook_url
        print(item)
        arr.append(item)
    result = link_collection.insert_many(arr)
    show_debug('Inserted')
    print(result.inserted_ids)
