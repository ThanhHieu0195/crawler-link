import pprint

from CrawlerLib.Pymongo import MongodbClient
from CrawlerLib.helper import get_master_attr
from CrawlerLib.server import get_master_option
from CrawlerLib.show_notify import show_debug, show_warning
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
            'ref': 'fb',
            'type': None
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

        try:
            show_debug('Call request: %s' % url)
            response = s.get(url, timeout=10)
        except requests.ConnectionError as err:
            show_warning(format(err))
            result['type'] = 'requests'
            result['msg'] = str(err)
        else:
            d = response.json()
            show_warning('Error fetch api fb')
            print(d)
            if get_master_attr('error', d, None) is None:
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
                result['type'] = 'api_fb_error'
                result['msg'] = get_master_attr('error.message', d, 'Error connect api fb')
                code = get_master_attr('error.code', d, None)
                if code == 190:
                    result['type'] = 'token'
                elif code == 100:
                    result['type'] = 'link_id'
        return result

    def process_response(self, result):
        show_debug('processing response ...')
        link = self.mongodb.get_link_collection().find_one({'link_id': result['data']['link_id']})
        collection_history = self.mongodb.get_link_history_collection()
        if link:
            item = {
                'likes': result['data']['likes'],
                'comments': result['data']['comments'],
                'reactions': result['data']['reactions'],
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

    def process_response_error(self, params, data):
        if data['type'] == 'token':
            self.__remove_token(params['token'])
            token = self.__get_token()
            if token is None:
                show_warning('All token expire')
                return None
            params['token'] = token['key']
            return {
                'reassign': True,
                'params': params
            }

        if data['type'] == 'link_id':
            link = self.mongodb.get_link_collection().find_one({'link_id': params['link_id']})
            if link:
                self.mongodb.get_link_collection().update_one({
                    '_id': link['_id']
                }, {
                    '$set': {
                        'status': 2,
                        'error': {
                            'message': 'not detach link id'
                        }
                    }
                })

        if data['type'] == 'requests':
            if 'proxy' in params:
                del params['proxy']
            return {
                'params': params,
                'reassign': True,
                'change_proxy': True,
                'remove_proxy': True
            }
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

    def __remove_token(self, token):
        def filter_token(t):
            return t['key'] != token
        self.tokens = list(filter(filter_token, self.tokens))
        return self.tokens
