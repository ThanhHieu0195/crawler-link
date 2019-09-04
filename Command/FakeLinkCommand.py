from CrawlerLib.Pymongo import MongodbClient
from Command.ICommand import ICommand
import time
from datetime import datetime


class FakeLinkCommand(ICommand):
    @staticmethod
    def get_name():
        return 'fake-link'

    def exec(self, args):
        data_links = [
            {
                "link_id": "100003803082906_1509228895880532",
                "type": "fb",
                "loop": [
                    datetime.fromtimestamp(time.time() + 60 * 0).strftime('%H:%M'),
                    datetime.fromtimestamp(time.time() + 60 * 1).strftime('%H:%M'),
                    datetime.fromtimestamp(time.time() + 60 * 3).strftime('%H:%M'),
                    datetime.fromtimestamp(time.time() + 60 * 5).strftime('%H:%M'),
                    datetime.fromtimestamp(time.time() + 60 * 7).strftime('%H:%M'),
                    datetime.fromtimestamp(time.time() + 60 * 9).strftime('%H:%M'),
                    datetime.fromtimestamp(time.time() + 60 * 11).strftime('%H:%M'),
                    datetime.fromtimestamp(time.time() + 60 * 13).strftime('%H:%M'),
                    datetime.fromtimestamp(time.time() + 60 * 15).strftime('%H:%M')
                ]
            },
            {
                "link_id": "BqkRJwMFtMb",
                "type": "ins",
                "loop": [
                    datetime.fromtimestamp(time.time() + 60 * 0).strftime('%H:%M'),
                    datetime.fromtimestamp(time.time() + 60 * 2).strftime('%H:%M'),
                    datetime.fromtimestamp(time.time() + 60 * 4).strftime('%H:%M'),
                    datetime.fromtimestamp(time.time() + 60 * 6).strftime('%H:%M'),
                    datetime.fromtimestamp(time.time() + 60 * 8).strftime('%H:%M'),
                    datetime.fromtimestamp(time.time() + 60 * 10).strftime('%H:%M'),
                    datetime.fromtimestamp(time.time() + 60 * 12).strftime('%H:%M'),
                    datetime.fromtimestamp(time.time() + 60 * 14).strftime('%H:%M')
                ]
            },
            {
                "link_id": "j8U06veqxdU",
                "type": "ytb",
                "loop": [
                    datetime.fromtimestamp(time.time() + 60 * 0).strftime('%H:%M'),
                    datetime.fromtimestamp(time.time() + 60 * 2).strftime('%H:%M'),
                    datetime.fromtimestamp(time.time() + 60 * 4).strftime('%H:%M'),
                    datetime.fromtimestamp(time.time() + 60 * 6).strftime('%H:%M'),
                    datetime.fromtimestamp(time.time() + 60 * 8).strftime('%H:%M'),
                    datetime.fromtimestamp(time.time() + 60 * 10).strftime('%H:%M'),
                    datetime.fromtimestamp(time.time() + 60 * 12).strftime('%H:%M'),
                    datetime.fromtimestamp(time.time() + 60 * 14).strftime('%H:%M')
                ]
            }
        ]
        result = []
        link_collection = MongodbClient.get_instance().get_link_collection()
        link_collection.drop()
        for link in data_links:
            result.append(link_collection.insert(link))

        return result
