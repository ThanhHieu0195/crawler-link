from Configs.enum import ServerConfig
from CrawlerLib.server import create_server, get_master_option
from CrawlerLib.show_notify import show_warning, show_info
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
                        result = self.task_assign(data['params'])
                        if result['error'] is False:
                            self.__notify_success(result['msg'])
                        else:
                            self.__notify_error(result['msg'])

                        _send(connection, {"action": "notify", "type": "success", "ref": "assign"})

                        while True:
                            data = _recev(connection)
                            if 'action' in data and data['action'] == 'assign':
                                result = self.task_assign(data['params'])
                                if result['error'] is False:
                                    self.__notify_success(result['msg'])
                                else:
                                    self.__notify_error(result['msg'])
                                _send(connection, {"action": "notify", "type": "success", "ref": "assign"})
                            else:
                                _send(connection, {"action": "notify", "type": "fail", "ref": "assign"})
                else:
                    self.__notify_error('format data error')
            except:
                self.__notify_error('Error waiting ... ')

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
        result = {'error': True, 'msg': ''}
        client = self.get_client(params)
        if client is None:
            result['msg'] = 'Not empty client subscribe'
            return result
        data = self.detectLinkProvider.format_request(params['type'], {
            'action': 'assign',
            'params': params
        })
        if data is not None:
            _send(client['cnn'], data)
            result['error'] = False
            result['msg'] = 'Run assign task - ' + params['link_id']
        else:
            result['msg'] = 'Type task not support'
            return result
        return result

    def get_client(self, params):
        clients = self.clients[params['type']]
        return get_master_option(clients)

    def __notify_error(self, msg):
        show_warning(msg)

    def __notify_success(self, msg):
        show_info(msg)
