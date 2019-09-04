import pprint
import re
from CrawlerLib.Pymongo import MongodbClient
from CrawlerLib.helper import get_master_attr
from CrawlerLib.server import get_master_option
from CrawlerLib.show_notify import show_debug, show_warning
from Facade.DetectLink.Plugin.ILink import ILink
import requests
import datetime

from Facade.Selemium.Selenium import Selenium


class FacebookLink(ILink):
    def __init__(self):
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
                    'likes': get_master_attr('likes.count', d, None),
                    'shares': get_master_attr('shares.count', d, None),
                    'comments': get_master_attr('comments.count', d, None),
                    'reactions': get_master_attr('reactions.summary.toal_count', d, None),
                    'created_time': get_master_attr('created_time', d, None),
                    'updated_at': str(datetime.datetime.utcnow())
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
        link_id = get_master_attr('data.link_id', result, None)

        # get user id
        matches = re.findall(r'(.*)_(.*)', link_id)
        user_id = None
        if len(matches):
            user_id = matches[0][0]

        link = self.mongodb.get_link_collection().find_one({'link_id': link_id})
        collection_history = self.mongodb.get_link_history_collection()
        if link:
            item = {
                'profile': {
                    'id': user_id,
                },
                'likes': result['data']['likes'],
                'comments': result['data']['comments'],
                'reactions': result['data']['reactions'],
                'shares': result['data']['shares'],
                'post_created_time': result['data']['created_time'],
                'updated_at': result['data']['updated_at']
            }

            # screenshot = Selenium.get_instance().screen_post('fb', link_id)
            # if screenshot:
            #     item['screenshot'] = screenshot

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

    def __get_token(self):
        self.__fetch_token()
        return get_master_option(self.tokens)

    def __remove_token(self, token):
        def filter_token(t):
            return t['key'] != token
        self._update_token(list(filter(filter_token, self.tokens)))
        return self.tokens

    def __fetch_token(self):
        f = open('Configs/facebooktoken')
        self.tokens = eval(f.read())
        f.close()
        return self.tokens

    def _update_token(self, tokens):
        f = open('Configs/facebooktoken', 'w')
        self.tokens = tokens
        f.write(str(tokens))
        f.close()
