from Configs.enum import ServerConfig
from CrawlerLib.helper import get_sys_params, get_master_attr, print_header_log
from CrawlerLib.server import create_server
import socket
import json
import re
from CrawlerLib.servercommand_helper import process_save_data_link, send_http_json_result, \
    process_download_attachment, send_http_result, process_take_info_link, get_info_request, process_update_link, \
    process_delete_link
from CrawlerLib.show_notify import show_text, show_warning, show_notify, show_debug

print_header_log()

params = get_sys_params()
port = get_master_attr('port', params, None)
num_client = get_master_attr('num_client', params, 3)

check = True
if port is None:
    print('Field port is required')

if num_client is None:
    print('Field num_client is required')

port = int(port)
num_client = int(num_client)


class ServerCommand:
    result = {"error": True, "msg": "", "data": None}

    def listen(self):
        s = create_server(ServerConfig.IP_ADDRESS.value, port, num_client)
        while True:
            try:
                connection, client_address = s.accept()
                data = b''
                connection.settimeout(0.5)
                show_text('====== NEW TASK =======')
                try:
                    while True:
                        try:
                            msg = connection.recv(1024)
                            if not msg:
                                break
                            data += msg
                            matches = re.findall(r'\r\n\r\n$', msg.decode())
                            if len(matches) > 0:
                                break
                        except socket.error:
                            break
                        except Exception as e:
                            print(e)
                            break
                    request_info = get_info_request(data.decode())
                    action = get_master_attr('query_params.1', request_info, None)

                    # process main action
                    if action == 'attachments':
                        self.process_attachment(connection)

                    if action == 'links':
                        self.process_links(connection, request_info)

                except Exception as e:
                    show_warning(format(e))
                    result = {"error": True, "msg": format(e)}
                    send_http_json_result(connection, result)
                connection.close()
            except socket.error as err:
                print(err)

    def init_result(self):
        self.result = {"error": True, "msg": "",  "data": None}

    def process_attachment(self, connection, request_info):
        show_debug('Process download attachment ...')
        self.init_result()
        if request_info['query_params'][2] is not None:
            self.result = process_download_attachment(request_info['query_params'][2])
            show_notify('Result')
            send_http_result(connection, self.result, content_type='image/png')
        else:
            print(1)

    def process_links(self, connection, request_info):
        self.init_result()
        method = request_info['method']
        if method == 'GET':
            self.result['error'] = False
            link_id = get_master_attr('query_params.2', request_info, None)
            self.result['data'] = process_take_info_link(link_id)
            send_http_json_result(connection, self.result)

        if method == 'POST':
            # process insert data
            show_debug('Insert link data')
            data = request_info['data']
            show_debug('data body')
            print(data)
            show_debug('Processing save data ...')
            self.result = process_save_data_link(data)
            show_notify('Success!')
            print(self.result)
            send_http_json_result(connection, self.result)

        if method == 'PUT':
            link_id = get_master_attr('query_params.2', request_info, None)
            show_debug('Edit link data: %s' % link_id)
            data = request_info['data']
            print(data)
            show_debug('Processing ... ')
            if link_id:
                result = process_update_link(link_id, data)
                if result:
                    self.result['msg'] = 'Updated'
                self.result['error'] = False
            send_http_json_result(connection, self.result)

        if method == 'DELETE':
            link_id = get_master_attr('query_params.2', request_info, None)
            show_debug('DELETE link data: %s' % link_id)
            show_debug('Processing ... ')
            if link_id:
                if process_delete_link(link_id):
                    self.result['msg'] = 'Deleted'
                self.result['error'] = False
            send_http_json_result(connection, self.result)

if check:
    servercommand = ServerCommand()
    servercommand.listen()
