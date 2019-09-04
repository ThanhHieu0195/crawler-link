import pymongo
from Configs.enum import ServerConfig


def connect_mongodb():
    return pymongo.MongoClient(ServerConfig.MONGO_HOST.value, ServerConfig.MONGO_PORT.value)


class MongodbClient:
    Client = None

    def __init__(self):
        self.mongodb = connect_mongodb()
        self.crawler_db = self.get_crawler_db()

    @staticmethod
    def get_instance():
        if MongodbClient.Client is None:
            MongodbClient.Client = MongodbClient()
        return MongodbClient.Client

    def is_connect(self):
        if self.mongodb is not None:
            return True
        return False

    def get_crawler_db(self):
        return self.mongodb[ServerConfig.MONGO_DATABASE.value]

    def get_collection(self, name):
        return self.get_crawler_db()[name]

    def get_link_collection(self):
        return self.get_collection('links')

    def get_link_history_collection(self):
        return self.get_collection('link_histories')
