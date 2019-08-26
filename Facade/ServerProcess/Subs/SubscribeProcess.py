from CrawlerLib.show_notify import show_info
from CrawlerLib.socketjson import _send
from Facade.ServerProcess.Subs.ISubProcess import ISubProcess


class SubscribeProcess(ISubProcess):
    @staticmethod
    def get_name():
        return 'subscribe'

    def process_sub(self, main, data):
        client_address = main.client_address
        connection = main.connection

        show_info(client_address[0] + " was subscribed with type " + data['type'])
        is_add = True
        if len(main.clients[data['type']]) > 0:
            for a in main.clients[data['type']]:
                if a['addr'] == client_address[0]:
                    a['cnn'] = connection
                    a['amount'] = 0
                    is_add = False
        if is_add:
            main.clients[data['type']].append({
                "addr": client_address[0],
                "cnn": connection,
                "amount": 0,
                "status": True
            })
        _send(connection, {"action": "notify", "type": "success", "ref": "subscribed"})
