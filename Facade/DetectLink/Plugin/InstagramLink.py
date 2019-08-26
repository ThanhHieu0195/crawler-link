import pprint

from CrawlerLib.Pymongo import MongodbClient
from CrawlerLib.helper import get_master_attr
from CrawlerLib.show_notify import show_debug
from Facade.DetectLink.Plugin.ILink import ILink
import requests
import json
import re
import time


class InstagramLink(ILink):
    def __init__(self):
        self.mongodb = MongodbClient.get_instance()

    @staticmethod
    def get_name():
        return 'ins'

    def format_request(self, data):
        return data

    def process_request(self, data):
        result = {
            'error': True,
            'msg': None,
            'data': None,
            'ref': 'ins'
        }
        url = 'https://www.instagram.com/p/' + data[
            'link_id']

        proxy = get_master_attr('proxy', data, None)
        s = requests.Session()
        if proxy:
            proxies = {
                "https": proxy,
                "http": proxy
            }
            s.proxies = proxies

        response = s.get(url)

        html = response.text
        regex = r"window._sharedData = {(.*)};</script>"
        matches = re.findall(regex, html, re.DOTALL)
        if matches:
            d = json.loads('{'+matches[0]+'}')
            result['error'] = False
            print(d)
            result['data'] = {
                'link_id': data['link_id'],
                'likes': get_master_attr('entry_data.PostPage.0.graphql.shortcode_media.edge_media_preview_like.count', d, None),
                'comments': get_master_attr('entry_data.PostPage.0.graphql.shortcode_media.edge_media_preview_comment.count', d, None),
                'created_time': get_master_attr('entry_data.PostPage.0.graphql.shortcode_media.taken_at_timestamp', d, None),
                'process_time': time.time()
            }
        return result

    def process_response(self, result):
        show_debug('processing response ...')
        link = self.mongodb.get_link_collection().find_one({'link_id': result['data']['link_id']})
        collection_history = self.mongodb.get_link_history_collection()
        if link:
            item = {
                'likes': result['data']['likes'],
                'comments': result['data']['comments'],
                'post_created_time': result['data']['created_time'],
                'last_update': result['data']['process_time']
            }
            res = self.mongodb.get_link_collection().update_one({
                '_id': link['_id']
            }, {
                '$set': item
            })
            item['link_id'] = result['data']['link_id']
            collection_history.insert_one(item)
            if res:
                return 1
            return 0
        return -1

