from abc import ABC, abstractmethod


class ISubProcess(ABC):
    @staticmethod
    @abstractmethod
    def get_name():
        pass

    @abstractmethod
    def process_sub(self, main, connection, client_address, data):
        pass
