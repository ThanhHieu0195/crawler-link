from Facade.DetectLink.Plugin.FacebookLink import FacebookLink


class DetectLink:
    def __init__(self):
        self.__plugins = {
            FacebookLink.get_name(): FacebookLink()
        }

    def process_request(self, type_link, data):
        if type_link not in self.__plugins:
            return None
        p = self.__plugins[type_link]
        return p.format_request(data)

    def process_response(self, type_link, response):
        if type_link not in self.__plugins:
            return None
        p = self.__plugins[type_link]
        return p.process_response(response)
