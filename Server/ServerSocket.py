from Configs.enum import ServerConfig
from CrawlerLib.server import create_server, get_master_option
from CrawlerLib.socketjson import _recev, _send
from Facade.DetectLink.DetectLink import DetectLink


class ServerSocket:
    def __init__(self):
        self.server = create_server(ServerConfig.IP_ADDRESS.value, ServerConfig.PORT.value, ServerConfig.NUM_CLIENT.value)
        self.clients = {
            "fb": [],
            "ins": [],
            "ytb": []
        }
        self.detectLinkProvider = DetectLink()

    def listen(self):
        while True:
            try:
                connection, client_address = self.server.accept()
                data = _recev(connection)
                if not data:
                    break
                if 'action' in data:
                    if data['action'] == 'subscribe':
                        self.task_subscribe(client_address, connection, data)
                    elif data['action'] == 'assign':
                        self.task_assign(data['params'])
                        print(data)
                        _send(connection, {"action": "notify", "type": "success", "ref": "assign"})

                        while True:
                            data = _recev(connection)
                            if 'action' in data and data['action'] == 'assign':
                                self.task_assign(data['params'])
                                _send(connection, {"action": "notify", "type": "success", "ref": "assign"})
                            else:
                                _send(connection, {"action": "notify", "type": "fail", "ref": "assign"})
                else:
                    self.__notify_error('format data error')
            except:
                print('Error')

    def task_subscribe(self, client_address, connection, data):
        self.__notify_success(client_address[0] + " was subscribed")
        self.clients[data['type']].append({
            "addr": client_address[0],
            "cnn": connection,
            "amount": 0,
            "status": True
        })
        _send(connection, {"action": "notify", "type": "success", "ref": "subscribed"})

    def task_assign(self, params):
        client = self.get_client(params)
        if client is None:
            self.__notify_error('Not empty client subscribe')

        data = self.detectLinkProvider.process_request(params['type'], {
            'action': 'assign',
            'params': params
        })
        if data is not None:
            _send(client['cnn'], data)
            self.__notify_success('assign task for ' + client['addr'])
        else:
            self.__notify_error('Type task not support')

    def get_client(self, params):
        clients = self.clients[params['type']]
        return get_master_option(clients)

    def __notify_error(self, msg):
        print(msg)

    def __notify_success(self, msg):
        print(msg)
