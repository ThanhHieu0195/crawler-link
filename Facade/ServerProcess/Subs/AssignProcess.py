from CrawlerLib.server import get_master_option
from CrawlerLib.show_notify import show_info, show_warning
from CrawlerLib.socketjson import _send, _recev
from Facade.DetectLink.DetectLink import DetectLink
from Facade.ServerProcess.Subs.ISubProcess import ISubProcess


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
        self.__process_data_result_task(connection, result)
        while True:
            data = _recev(connection)
            if 'action' in data and data['action'] == 'assign':
                result = self.__task_assign(data['params'])
                self.__process_data_result_task(connection, result)
            else:
                _send(connection, {"action": "notify", "type": "fail", "ref": "assign"})

    def process_response(self, response):
        if response['error'] == False:
            self.detectLinkProvider.process_response(response['ref'], response)
        else:
            print(response)

    def __process_data_result_task(self, connection, r):
        if r['error'] is False:
            show_info(r['msg'])
        else:
            show_warning(r['msg'])

    def __task_assign(self, params):
        result = {'error': True, 'msg': ''}
        client = self.__get_client(params)
        if client is None:
            result['msg'] = 'Not empty client subscribe'
            return result
        data = self.detectLinkProvider.format_request(params['type'], {
            'action': 'assign',
            'params': params
        })
        if data is not None:
            result['error'] = False
            result['msg'] = 'Run assign task - ' + params['link_id']
            _send(client['cnn'], data)
            self.process_response(_recev(client['cnn']))
        else:
            result['msg'] = 'Type task not support'
            return result
        return result

    def __get_client(self, params):
        clients = self.main.clients[params['type']]
        return get_master_option(clients)