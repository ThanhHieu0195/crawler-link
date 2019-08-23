from abc import ABC, abstractmethod


class ICommand(ABC):
    @staticmethod
    @abstractmethod
    def get_name():
        pass

    @abstractmethod
    def exec(self, args):
        pass
