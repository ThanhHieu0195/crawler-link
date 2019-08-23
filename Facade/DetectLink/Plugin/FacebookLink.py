from CrawlerLib.server import get_master_option
from Facade.DetectLink.Plugin.ILink import ILink
from Configs.constant import FACEBOOK_TOKEN
import requests


class FacebookLink(ILink):
    def __init__(self):
        self.__init_tokens()

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
        url = 'https://graph.facebook.com/' + data[
            'link_id'] + '?fields=reactions.summary(true),comments.summary(true),shares,likes&access_token=' + data[
                  'token']
        print(url)
        return requests.get(url)

    def process_response(self, result):
        return True

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
