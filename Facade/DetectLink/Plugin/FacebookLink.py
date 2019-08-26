import pprint

from CrawlerLib.Pymongo import MongodbClient
from CrawlerLib.helper import get_master_attr
from CrawlerLib.server import get_master_option
from CrawlerLib.show_notify import show_debug
from Facade.DetectLink.Plugin.ILink import ILink
from Configs.constant import FACEBOOK_TOKEN
import requests
import time


class FacebookLink(ILink):
    def __init__(self):
        self.__init_tokens()
        self.mongodb = MongodbClient.get_instance()

    @staticmethod
    def get_name():
        return 'fb'

    def format_request(self, data):
        token = self.__get_token()
        if token is None:
            return None
        data['params']['token'] = token['key']
        return data

    def process_request(self, data):
        result = {
            'error': True,
            'msg': None,
            'data': None,
            'ref': 'fb'
        }
        url = 'https://graph.facebook.com/' + data[
            'link_id'] + '?fields=reactions.summary(true),comments.summary(true),shares,likes&access_token=' + data[
                  'token']
        proxy = get_master_attr('proxy', data, None)
        s = requests.Session()
        if proxy:
            proxies = {
                "https": proxy,
                "http": proxy
            }
            s.proxies = proxies
        response = s.get(url)
        if response:
            d = response.json()
            result['error'] = False
            result['data'] = {
                'link_id': data['link_id'],
                'likes': d['likes']['count'],
                'comments': d['comments']['count'],
                'reactions': d['reactions']['summary']['total_count'],
                'created_time': d['created_time'],
                'process_time': time.time()
            }
        else:
            d = response.json()
            result['msg'] = d['error']['message']
        return result

    def process_response(self, result):
        show_debug('processing response ...')
        link = self.mongodb.get_link_collection().find_one({'link_id': result['data']['link_id']})
        collection_history = self.mongodb.get_link_history_collection()
        if link:
            print(result)
            item = {
                'likes': result['data']['likes'],
                'comments': result['data']['comments'],
                'reactions': result['data']['reactions'],
                'post_created_time': result['data']['created_time'],
                'last_update': result['data']['process_time']
            }
            print(item)
            res = self.mongodb.get_link_collection().update_one({
                '_id': link['_id']
            }, {
                '$set': item
            })
            pprint.pprint(res)
            item['link_id'] = result['data']['link_id']
            collection_history.insert_one(item)

            if res:
                return 1
            return 0
        return -1

    def process_response_error(self, data):
        return None

    def __init_tokens(self):
        self.tokens = []
        for t in FACEBOOK_TOKEN:
            self.tokens.append({
                'status': True,
                'amount': 0,
                'key': t
            })

    def __get_token(self):
        return get_master_option(self.tokens)
