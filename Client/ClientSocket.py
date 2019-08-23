from CrawlerLib.client import create_client
from CrawlerLib.socketjson import _recev, _send
from Configs.enum import ServerConfig


class ClientSocket:
    def __init__(self):
        client = create_client(ServerConfig.IP_ADDRESS.value, ServerConfig.PORT.value)
        _send(client, {"action": "subscribe", "type": ServerConfig.CLIENT_TYPE.value})
        self.client = client

    def listen(self):
        while True:
            data = _recev(self.client)
            if "action" in data:
                if data['action'] == 'notify' and data['ref'] == 'subscribed':
                    print("subscribe was successfully")

                if data['action'] == 'assign':
                    self.do_assign(data)

    def do_assign(self, data):
        print(data)
