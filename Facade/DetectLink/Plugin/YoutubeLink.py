import pprint

from Configs.enum import ServerConfig
from CrawlerLib.Pymongo import MongodbClient
from CrawlerLib.helper import get_master_attr
from CrawlerLib.show_notify import show_debug
from Facade.DetectLink.Plugin.ILink import ILink
import requests
import json
import re
import time


class YoutubeLink(ILink):
    def __init__(self):
        self.mongodb = MongodbClient.get_instance()

    @staticmethod
    def get_name():
        return 'ytb'

    def format_request(self, data):
        return data

    def process_request(self, data):
        result = {
            'error': True,
            'msg': None,
            'data': None,
            'ref': YoutubeLink.get_name()
        }
        url = 'https://www.googleapis.com/youtube/v3/videos?part=statistics&id=%s&key=%s' % (data['link_id'], ServerConfig.API_YTB_KEY.value)
        response = requests.get(url)
        d = response.json()

        if 'error' not in d:
            result['error'] = False
            print(d)
            result['data'] = {
                'link_id': data['link_id'],
                'dislikes': get_master_attr('items.0.statistics.likeCount', d, None),
                'likes': get_master_attr('items.0.statistics.dislikeCount', d, None),
                'views': get_master_attr('items.0.statistics.viewCount', d, None),
                'comments': get_master_attr('items.0.statistics.commentCount', d, None),
                'created_time': None,
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
                'views': result['data']['views'],
                'dislikes': result['data']['dislikes'],
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

