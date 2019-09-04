from abc import ABC, abstractmethod


class ILink(ABC):
    @staticmethod
    @abstractmethod
    def get_name():
        pass

    @abstractmethod
    def format_request(self, data):
        pass

    def process_request(self, data):
        pass

    def process_response(self, result):
        pass

    def process_response_error(self, params, response):
        pass
