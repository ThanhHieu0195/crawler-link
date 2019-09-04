from CrawlerLib.show_notify import show_debug
from Facade.DetectLink.Plugin import YoutubeLink
from Facade.DetectLink.Plugin.FacebookLink import FacebookLink
from Facade.DetectLink.Plugin.InstagramLink import InstagramLink
from Facade.DetectLink.Plugin.YoutubeLink import YoutubeLink


class DetectLink:
    Main = None

    def __init__(self):
        self.__plugins = {
            FacebookLink.get_name(): FacebookLink(),
            InstagramLink.get_name(): InstagramLink(),
            YoutubeLink.get_name(): YoutubeLink(),
        }

    @staticmethod
    def get_instance():
        if DetectLink.Main is None:
            DetectLink.Main = DetectLink()
        return DetectLink.Main

    def format_request(self, type_link, data):
        if type_link not in self.__plugins:
            return None
        p = self.__plugins[type_link]
        return p.format_request(data)

    def process_request(self, type_link, data):
        show_debug('processing with params ...')
        print(data)
        if type_link not in self.__plugins:
            return None
        p = self.__plugins[type_link]
        return p.process_request(data)

    def process_response(self, type_link, response):
        if type_link not in self.__plugins:
            return None
        p = self.__plugins[type_link]
        return p.process_response(response)

    def process_response_error(self, type_link, params, response):
        if type_link not in self.__plugins:
            return None
        p = self.__plugins[type_link]
        return p.process_response_error(params, response)
