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


def process_download_attachment(attachment_name):
    f = open('Screenshot/%s.png' % attachment_name, 'rb')
    content = f.read()
    f.close()
    return content


def process_save_data_link(data):
    result = {"error": False, "msg": "Completed", 'data': []}
    mongodb = MongodbClient.get_instance()
    link_collection = mongodb.get_link_collection()

    items = get_master_attr('body', data, [])
    hook_url = get_master_attr('hook_url', data, None)
    for item in items:
        # format deadline
        matches = re.findall(r'(\d{4})(\d{2})(\d{2})', item['deadline'])
        if len(matches) > 0:
            item['deadline'] = datetime.datetime(int(matches[0][0]), int(matches[0][1]), int(matches[0][2]))
        else:
            item['deadline'] = datetime.datetime.utcnow()

        # format deadline start
        matches = re.findall(r'(\d{4})(\d{2})(\d{2})', get_master_attr('camp_start', item, ''))
        if len(matches) > 0:
            item['camp_start'] = datetime.datetime(int(matches[0][0]), int(matches[0][1]), int(matches[0][2]))
        else:
            item['camp_start'] = datetime.datetime(datetime.datetime.utcnow().year, datetime.datetime.utcnow().month,
                                                   datetime.datetime.utcnow().day)

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
        # item['deadline'] = datetime.datetime.utcnow()
        item['status'] = 1
        item['hook_url'] = hook_url
        try:
            result['data'].append({
                'msg': 'Success',
                'error': False,
                'link_id': item['link_id']
            })
            link_collection.insert(item)
        except pymongo.errors.DuplicateKeyError as e:
            del item['_id']
            link_collection.update({
                'link_id': item['link_id']
            }, {'$set': item})
            result['data'].append({
                'msg': 'Replace',
                'error': False,
                'link_id': item['link_id']
            })
        except Exception as e:
            result['data'].append({
                'msg': format(e),
                'error': True,
                'link_id': item['link_id']
            })
    return result


def send_http_result(response, result, content_type='text/html'):
    msg = result
    response_headers = {
        'Content-Type': content_type,
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
    msg_max = len(msg)
    start = 0
    end = 1024
    while msg_max >= start:
        response.send(msg[start:end])
        start = end
        end += 1024


def send_http_json_result(response, result):
    msg = json.dumps(result, default=str)
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


def get_info_request(data):
    json_string = detect_json(data)
    if json_string is None:
        json_string = '{}'
    return {
        'query_params': get_query_params(data),
        'method': get_method(data),
        'data': json.loads(json_string)
    }


def get_query_params(data):
    matches = re.findall(r'^[a-zA-Z]+ (.*) ', data)
    if len(matches):
        path = matches[0]
        return path.split('/')
    return None


def get_method(data):
    matches = re.findall(r'^[a-zA-Z]+', data)
    if len(matches):
        return matches[0]
    return None


def process_take_info_link(link_id):
    mongodb = MongodbClient.get_instance()
    link_collection = mongodb.get_link_collection()
    if link_id is None:
        link = list(link_collection.find())
    else:
        link = link_collection.find_one({"link_id": link_id})
    return link


def process_update_link(link_id, data):
    allow_keys = ['link_id', 'status', 'type']
    mongodb = MongodbClient.get_instance()
    link_collection = mongodb.get_link_collection()
    link = link_collection.find_one({'link_id': link_id})
    params = {}
    if link:
        for key in allow_keys:
            value = get_master_attr(key, data, None)
            if value is not None:
                params[key] = value

        return link_collection.update({'_id': link['_id']}, {"$set": params})

    return None


def process_delete_link(link_id):
    mongodb = MongodbClient.get_instance()
    link_collection = mongodb.get_link_collection()
    return link_collection.delete_one({'link_id': link_id})
