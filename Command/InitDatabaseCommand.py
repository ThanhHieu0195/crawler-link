import pymongo
import bson
from Command.ICommand import ICommand
from CrawlerLib.Pymongo import MongodbClient
import time


class InitDatabaseCommand(ICommand):
    @staticmethod
    def get_name():
        return 'init-db'

    def exec(self, argv):
        db = MongodbClient.get_instance().get_crawler_db()
        #  drop database
        db.links.drop()
        db.create_collection('links')
        print('drop database')
        # init database
        data_command = {
                "collMod": "links",
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["link_id", "type"],
                        "properties": {
                            "type": {
                                "enum": ["FB", "IG", "YT"],
                                "description": "can only be one of enum values [FB, IN, YT] and is required"
                                },
                            "link_id": {
                                "bsonType": "string",
                                "description": "must be a string and required"
                                }
                            }
                        }
                    }
                }
        db.command(data_command)
        db['links'].create_index([('link_id', pymongo.TEXT)], unique=True)
        return None
