from Configs.enum import ServerConfig
from CrawlerLib.helper import get_sys_params, get_master_attr, print_header_log
from CrawlerLib.server import create_server
import socket
import json
import re
from CrawlerLib.servercommand_helper import detect_json, process_save_data_link, send_http_json_result, \
    process_download_attachment, send_http_result, get_query_params, process_take_info_link, get_info_request
from CrawlerLib.show_notify import show_text, show_warning, show_notify, show_debug
import time

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

if check:
    s = create_server(ServerConfig.IP_ADDRESS.value, port, num_client)
    while True:
        try:
            connection, client_address = s.accept()
            data = b''
            connection.settimeout(0.5)
            show_text('====== NEW TASK =======')
            try:
                result = {"error": True, "msg": "Fail"}
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
                if len(request_info['query_params']) >= 2 and request_info['query_params'][1] != '':
                    if request_info['query_params'][1] == 'attachments':
                        show_debug('Process download attachment ...')
                        if request_info['query_params'][2] is not None:
                            result = process_download_attachment(request_info['query_params'][2])
                            show_notify('Result')
                            send_http_result(connection, result)

                    if request_info['query_params'][1] == 'links':
                        if request_info['method'] == 'GET':
                            show_debug('Process take info links')
                            print(request_info['query_params'][2])
                            result = process_take_info_link(request_info['query_params'][2])
                            send_http_json_result(connection, result)
                        else:
                            data = json.loads(request_info['data'])
                            show_debug('Body request')
                            print(request_info['data'])
                            show_debug('Process save data link ...')
                            result = process_save_data_link(data)
                            show_notify('Result')
                            print(result)
                            send_http_json_result(connection, result)
            except Exception as e:
                show_warning(format(e))
                result = {"error": True, "msg": format(e)}
                send_http_json_result(connection, result)
            connection.close()
        except socket.error as err:
            print(err)

