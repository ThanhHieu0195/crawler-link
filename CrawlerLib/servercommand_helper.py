import re
import json
from CrawlerLib.Pymongo import MongodbClient
from CrawlerLib.helper import get_master_attr
from CrawlerLib.show_notify import show_debug
import datetime
import pymongo
from pymongo import errors


def detect_json(json_text):
    matches = re.findall(r'{(.*)}', json_text, re.DOTALL)
    if matches:
        return '{%s}' % matches[0]
    return None


def process_save_data_link(data):
    result = {"error": True, "msg": "Fail"}
    mongodb = MongodbClient.get_instance()
    link_collection = mongodb.get_link_collection()

    items = get_master_attr('body', data, [])
    hook_url = get_master_attr('hook_url', data, None)
    arr = []
    for item in items:
        # format deadline
        matches = re.findall(r'(\d{4})(\d{2})(\d{2})', item['deadline'])
        if len(matches) > 0:
            item['deadline'] = datetime.datetime(int(matches[0][0]), int(matches[0][1]), int(matches[0][2]))
        else:
            item['deadline'] = datetime.datetime.utcnow()

        # format timeline
        timeline = get_master_attr('timeline', item, [])
        if len(timeline) > 0:
            count = 0
            for itime in timeline:
                matches = re.findall(r'(\d{2}):(\d{2})', itime)
                if len(matches) > 0:
                    timeline[count] = '%s:00' % matches[0][0]
                else:
                    timeline[count] = '00:00'
                count += 1
        item['timeline'] = timeline
        item['created_at'] = datetime.datetime.utcnow()
        item['updated_at'] = datetime.datetime.utcnow()
        item['deadline'] = datetime.datetime.utcnow()
        item['status'] = 1
        item['hook_url'] = hook_url
        arr.append(item)
    try:
        data_result = link_collection.insert_many(arr)
    except pymongo.errors.DuplicateKeyError as e:
        result['msg'] = format(e)
    except Exception as e:
        result['msg'] = format(e)
    else:
        result['error'] = False
        result['msg'] = len(list(data_result.inserted_ids))
    return result


def send_http_result(response, result):
    msg = json.dumps(result)
    response_headers = {
        'Content-Type': 'application/json; encoding=utf8',
        'Content-Length': len(msg),
        'Connection': 'close',
    }
    response_headers_raw = ''.join('%s: %s\r\n' % (k, v) for k, v in response_headers.items())
    response_proto = 'HTTP/1.1'
    response_status = '200'
    response_status_text = 'OK'  # this can be random
    r = '%s %s %s\r\n' % (response_proto, response_status, response_status_text)
    response.send(r.encode())
    response.send(response_headers_raw.encode())
    response.send(b'\r\n')  # to separate headers from body
    response.send(msg.encode(encoding="utf-8"))
