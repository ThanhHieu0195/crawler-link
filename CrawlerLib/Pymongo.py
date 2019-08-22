import pymongo
from Configs.enum import ServerConfig


def connect_mongo():
    return pymongo.MongoClient(ServerConfig.MONGO_HOST.value, ServerConfig.MONGO_PORT.value)
