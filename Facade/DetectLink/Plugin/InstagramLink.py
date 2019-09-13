import pprint

from CrawlerLib.Pymongo import MongodbClient
from CrawlerLib.helper import get_master_attr
from CrawlerLib.show_notify import show_debug, show_warning
from Facade.DetectLink.Plugin.ILink import ILink
import requests
import json
import re
import datetime

from Facade.Selemium.Selenium import Selenium


class InstagramLink(ILink):
    def __init__(self):
        self.mongodb = MongodbClient.get_instance()

    @staticmethod
    def get_name():
        return 'IG'

    def format_request(self, data):
        return data

    def process_request(self, data):
        result = {
            'error': True,
            'msg': None,
            'data': None,
            'ref': 'IG'
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

        try:
            response = s.get(url, timeout=10)
        except requests.ConnectionError as err:
            result['type'] = 'requests'
            result['msg'] = str(err)
        else:
            html = response.text
            regex = r"window._sharedData = {(.*)};</script>"
            matches = re.findall(regex, html, re.DOTALL)
            if matches:
                d = json.loads('{'+matches[0]+'}')
                result['error'] = False
                result['data'] = {
                    'link_id': data['link_id'],
                    'likes': get_master_attr('entry_data.PostPage.0.graphql.shortcode_media.edge_media_preview_like.count', d, None),
                    'comments': get_master_attr('entry_data.PostPage.0.graphql.shortcode_media.edge_media_preview_comment.count', d, None),
                    'created_time': get_master_attr('entry_data.PostPage.0.graphql.shortcode_media.taken_at_timestamp', d, None),
                    'updated_at': str(datetime.datetime.utcnow()),
                    'profile': {
                        'id': get_master_attr('entry_data.PostPage.0.graphql.shortcode_media.owner.id', d, None),
                        'username': get_master_attr('entry_data.PostPage.0.graphql.shortcode_media.owner.username', d, None),
                        'display_name': get_master_attr('entry_data.PostPage.0.graphql.shortcode_media.owner.full_name', d,
                                                    None)
                    }

                }
            else:
                result['msg'] = 'Not detect link'
                result['type'] = 'link_id'
        return result

    def process_response(self, result):
        show_debug('processing response ...')
        link = self.mongodb.get_link_collection().find_one({'link_id': result['data']['link_id']})
        collection_history = self.mongodb.get_link_history_collection()
        if link:
            item = {
                'profile': get_master_attr('data.profile', result, None),
                'likes': result['data']['likes'],
                'comments': result['data']['comments'],
                'post_created_time': result['data']['created_time'],
                'updated_at': result['data']['updated_at']
            }

            # screenshot
            Selenium.get_instance().screen_post('IG', result['data']['link_id'])
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
