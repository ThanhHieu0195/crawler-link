from CrawlerLib.client import create_client
from CrawlerLib.socketjson import _recev, _send
from Configs.enum import ServerConfig
import time

class ClientSocket():
    def __init__(self):
        client = create_client(ServerConfig.IPADDRESS.value, ServerConfig.PORT.value)
        _send(client, {"action": "subscribe"})
        self.client = client

    def listen(self):
        while True:
            data = _recev(self.client)
            print(data)
            time.sleep(1)