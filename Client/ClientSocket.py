from CrawlerLib.client import create_client
from CrawlerLib.socketjson import _recev, _send
from Configs.enum import ServerConfig
from Facade.DetectLink.DetectLink import DetectLink


class ClientSocket:
    def __init__(self):
        client = create_client(ServerConfig.IP_ADDRESS.value, ServerConfig.PORT.value)
        _send(client, {"action": "subscribe", "type": ServerConfig.CLIENT_TYPE.value})
        self.client = client
        self.detectLinkProvider = DetectLink()

    def listen(self):
        while True:
            data = _recev(self.client)
            if "action" in data:
                if data['action'] == 'notify' and data['ref'] == 'subscribed':
                    print("subscribe was successfully")

                if data['action'] == 'assign':
                    self.do_assign(data['params'])

    def do_assign(self, data):
        res = self.detectLinkProvider.process_request(data['type'], data)
        print(res)
