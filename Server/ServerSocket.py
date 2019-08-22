from CrawlerLib.server import create_server
from CrawlerLib.socketjson import _recev, _send
from Configs.enum import ServerConfig


class ServerSocket:
    def __init__(self):
        self.server = create_server(ServerConfig.IP_ADDRESS.value, ServerConfig.PORT.value, ServerConfig.NUM_CLIENT.value)
        self.clients = {
            "fb": [],
            "ins": [],
            "ytb": []
        }

    def listen(self):
        while True:
            connection, client_address = self.server.accept()
            data = _recev(connection)
            if 'action' in data:
                if data['action'] == 'subscribe':
                    self.task_subscribe(client_address, connection, data)
                elif data['action'] == 'assign':
                    self.task_asign(data['params'])
            else:
                print('Error data: ', data)

    def task_subscribe(self, client_address, connection, data):
        print("subscribe by " + client_address[0])
        print(data)
        self.clients[data['type']].append({
            "addr": client_address[0],
            "cnn": connection
        })
        _send(connection, {"action": "success"})

    def task_asign(self, params):
        client = self.get_client(params)
        _send(client['cnn'], params)
        print('assign task for ' + client['addr'])

    def get_client(self, params):
        clients = self.clients[params['type']]
        return clients[0]
