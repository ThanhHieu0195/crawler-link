from CrawlerLib.server import get_master_option
from Facade.DetectLink.Plugin.ILink import ILink
from Configs.constant import FACEBOOK_TOKEN


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
        data['token'] = token
        return data

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
