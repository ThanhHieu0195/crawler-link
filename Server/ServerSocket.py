from CrawlerLib.server import create_server
from CrawlerLib.socketjson import _recev, _send
from Configs.enum import ServerConfig

class ServerSocket():
    def __init__(self):
        self.server = create_server(ServerConfig.IPADDRESS.value, ServerConfig.PORT.value, ServerConfig.NUMCLIENT.value)
        self.clients = {
            "fb": [],
            "ins": [],
            "ytb": []
        }

    def listen(self):
        while True:
            connection, client_address = self.server.accept()
            data = _recev(connection)
            if data['action'] == 'subscribe':
                print("subscribe by " + client_address[0])
                ipaddress = client_address[0]
                self.clients[client_address[0]] = connection
                _send(connection, {"action": "msg", "msg": "ok"})
            elif data['action'] == 'assign':
                type = data['type']
                # _send(self.clients[addr], {"action": "assign", "task": "crawler fb"})