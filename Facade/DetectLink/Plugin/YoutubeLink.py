import pprint

from Configs.enum import ServerConfig
from CrawlerLib.Pymongo import MongodbClient
from CrawlerLib.helper import get_master_attr
from CrawlerLib.show_notify import show_debug, show_warning
from Facade.DetectLink.Plugin.ILink import ILink
import requests
import json
import re
import datetime

from Facade.Selemium.Selenium import Selenium


class YoutubeLink(ILink):
    def __init__(self):
        self.mongodb = MongodbClient.get_instance()

    @staticmethod
    def get_name():
        return 'YT'

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
        except requests.HTTPError as err:
            show_warning(format(err))
        else:
            d = response.json()
            if 'error' not in d:
                result['error'] = False
                result['data'] = {
                    'link_id': data['link_id'],
                    'dislikes': get_master_attr('items.0.statistics.likeCount', d, None),
                    'likes': get_master_attr('items.0.statistics.dislikeCount', d, None),
                    'views': get_master_attr('items.0.statistics.viewCount', d, None),
                    'comments': get_master_attr('items.0.statistics.commentCount', d, None),
                    'created_time': None,
                    'updated_at': str(datetime.datetime.utcnow())
                }
            else:
                result['msg'] = get_master_attr('error.errors.0.message', d, 'Error from api youtube')
                if get_master_attr('error.code', d, None) == 400:
                    if get_master_attr('error.errors.0.reason', d, None) == 'keyInvalid':
                        result['type'] = 'api_key'
                        result['msg'] = 'Api key error'
                    else:
                        result['type'] = 'link_id'
                        result['msg'] = 'Link id error'

                else:
                    result['type'] = 'youtube_error'

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
                'updated_at': result['data']['updated_at']
            }

            # screenshot
            Selenium.get_instance().screen_post('YT', result['data']['link_id'])
            item['processing_screenshot'] = 1
            item['screenshot'] = None

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

