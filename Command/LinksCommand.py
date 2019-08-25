from CrawlerLib.Pymongo import MongodbClient
from Command.ICommand import ICommand
import pprint


class LinksCommand(ICommand):
    @staticmethod
    def get_name():
        return 'links'

    def exec(self, args):
        if 'link_id' in args:
            link= MongodbClient.get_instance().get_link_collection().find_one({'link_id': args['link_id']})
            pprint.pprint(link)
            print('histories:')
            histories = MongodbClient.get_instance().get_link_history_collection().find({'link_id': args['link_id']})
            pprint.pprint(list(histories))
        else:
            links = MongodbClient.get_instance().get_link_collection().find()
            for link in links:
               pprint.pprint(link)
        return None
