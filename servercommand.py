from Configs.enum import ServerConfig
from CrawlerLib.helper import get_sys_params, get_master_attr, print_header_log
from CrawlerLib.server import create_server
import socket
import json

from CrawlerLib.servercommand_helper import detect_json, process_save_data_link, send_http_result
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

if check:
    s = create_server(ServerConfig.IP_ADDRESS.value, port, num_client)
    while True:
        try:
            connection, client_address = s.accept()
            data = b''
            connection.settimeout(1.5)
            show_text('====== NEW TASK =======')
            try:
                result = {"error": True, "msg": "Fail"}
                while True:
                    try:
                        data += connection.recv(1024)
                    except socket.error:
                        break
                sjson = detect_json(data.decode())
                show_debug('Body request')
                print(sjson)
                if sjson:
                    data = json.loads(sjson)
                    result = process_save_data_link(data)

                show_notify('Result')
                print(result)
                send_http_result(connection, result)
            except Exception as e:
                show_warning(format(e))
                result['msg'] = format(e)
                send_http_result(connection, result)
            connection.close()
        except socket.error as err:
            print(err)

