import pymongo

from Command.ICommand import ICommand
from CrawlerLib.Pymongo import MongodbClient


class InitDatabaseCommand(ICommand):
    @staticmethod
    def get_name():
        return 'init-db'

    def exec(self, argv):
        db = MongodbClient.get_instance().get_crawler_db()
        #  drop database
        db['links'].drop()
        # init database
        db.create_collection('links')
        db['links'].create_index([('link_id', pymongo.TEXT)], unique=True)
        return None
