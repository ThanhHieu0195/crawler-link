from Configs.enum import ServerConfig
from CrawlerLib.helper import get_master_attr, update_proxies, fetch_proxies
from CrawlerLib.server import get_master_option
from CrawlerLib.show_notify import show_notify, show_warning, show_debug
from CrawlerLib.socketjson import _send, _recev
from Facade.DetectLink.DetectLink import DetectLink
from Facade.ServerProcess.Subs.ISubProcess import ISubProcess
import socket as socket_lib


class AssignProcess(ISubProcess):
    def __init__(self):
        self.detectLinkProvider = DetectLink.get_instance()

    @staticmethod
    def get_name():
        return 'assign'

    def process_sub(self, main, data):
        self.main = main
        connection = main.connection
        result = self.__task_assign(data['params'])
        _send(connection, {"action": "notify", "type": "success", "ref": "assign"})
        self.__process_data_result_task(result)
        while True:
            data = _recev(connection)
            if 'action' in data and data['action'] == 'assign':
                result = self.__task_assign(data['params'])
                self.__process_data_result_task(result)
                _send(connection, {"action": "notify", "type": "success", "ref": "assign"})
            else:
                _send(connection, {"action": "notify", "type": "fail", "ref": "assign"})

    def process_response(self, client, proxy, data, response):
        if response and get_master_attr('error', response, False) == False:
            self.detectLinkProvider.process_response(response['ref'], response)
            return {
                'error': False,
                'msg': 'task process success'
            }
        else:
            params = data['params']
            result_error = self.detectLinkProvider.process_response_error(params['type'], params, response)
            if result_error is None:
                return {
                    'error': True,
                    'msg': get_master_attr('msg', response, 'task process error')
                }

            if 'reassign' in result_error and result_error['reassign']:
                show_debug('reassign task %s' % params['link_id'])
                if 'remove_proxy' in result_error and result_error['remove_proxy'] is True:
                    self._remove_proxy(proxy)

                if 'change_proxy' in result_error and result_error['change_proxy'] is True:
                    proxy = self.__get_proxy()

                data['params'] = result_error['params']
                return self._execute_task(client, proxy, data)

    def __process_data_result_task(self, r):
        if r['error'] is False:
            show_notify(r['msg'])
        else:
            show_warning(r['msg'])

    def __task_assign(self, params):
        show_notify('Task assign running - %s' % params['link_id'])
        client = self.__get_client(params)
        proxy = self.__get_proxy()
        if proxy:
            params['proxy'] = proxy['proxy']
        data = self.detectLinkProvider.format_request(params['type'], {
            'action': 'assign',
            'params': params
        })
        return self._execute_task(client, proxy, data)

    def _execute_task(self, client, proxy, data):
        result = {'error': True, 'msg': 'Type task not support'}
        if data is not None:
            if proxy:
                data['params']['proxy'] = proxy['proxy']

            if client is None:
                result['msg'] = 'Client empty with task %s' % data['params']['link_id']
                return result

            _send(client['cnn'], data)
            response = _recev(client['cnn'], None)
            if response:
                return self.process_response(client, proxy, data, response)
            else:
                result['msg'] = 'time out. Client not response'
        return result

    def __get_client(self, params):
        clients = self.main.clients[params['type']]
        client = get_master_option(clients)
        if client:
            while client is not None and AssignProcess.check_client(client['cnn']) is False:
                clients = self._remove_client(params['type'], client)
                client = get_master_option(clients)
        return client

    def __get_proxy(self):
        return get_master_option(fetch_proxies())

    def _remove_proxy(self, proxy):
        def filter_proxy(x):
            return x != proxy
        return update_proxies(list(filter(filter_proxy, fetch_proxies())))

    def _remove_client(self, client_type, client):
        def filter_client(x):
            return x != client

        self.main.clients[client_type] = list(filter(filter_client, self.main.clients[client_type]))
        return self.main.clients

    @staticmethod
    def check_client(client):
        try:
            client.settimeout(3)
            _send(client, {'action': 'live'})
            client.recv(1024)
        except socket_lib.error as e:
            client.settimeout(int(ServerConfig.TIME_OUT.value))
            return False
        else:
            client.settimeout(int(ServerConfig.TIME_OUT.value))
            return True

