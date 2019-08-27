from CrawlerLib import show_notify
from CrawlerLib.client import create_client
from CrawlerLib.helper import get_sys_params, get_master_attr
from CrawlerLib.show_notify import show_debug, show_warning, show_notify, show_text
from CrawlerLib.socketjson import _recev, _send
from Configs.enum import ServerConfig
from Facade.DetectLink.DetectLink import DetectLink


class ClientSocket:
    def __init__(self):
        client_type = ServerConfig.CLIENT_TYPE.value
        params = get_sys_params()
        if 'type' in params:
            client_type = params['type']
        client = create_client(ServerConfig.IP_ADDRESS.value, ServerConfig.PORT.value)
        _send(client, {"action": "subscribe", "type": client_type})
        self.client = client
        self.detectLinkProvider = DetectLink()

    def listen(self):
        while True:
            try:
                data = _recev(self.client)
                if "action" in data:
                    if data['action'] == 'notify' and data['ref'] == 'subscribed':
                        show_notify("subscribe was successfully")

                    if data['action'] == 'assign':
                        show_text('== NEW TASK Assign ===')
                        show_debug('Receiver assign task with link %s' % get_master_attr('params.link_id', data, None))
                        self.do_assign(data['params'])

                    if data['action'] == 'live':
                        _send(self.client, {
                            'action': 'live',
                            'status': True
                        })
            except ConnectionError as err:
                show_warning("OS error: {0}".format(err))

    def do_assign(self, data):
        res = self.detectLinkProvider.process_request(data['type'], data)
        res['action'] = 'detect-link'
        show_debug('Result response process request ...')
        print(res)
        _send(self.client, res)
