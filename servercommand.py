from Configs.enum import ServerConfig
from CrawlerLib.helper import get_sys_params, get_master_attr
from CrawlerLib.server import create_server
import socket
import time
import json
import pprint

from CrawlerLib.servercommand_helper import detect_json, process_save_data_link

print("=========================================")
print("Today: " + time.strftime('%d-%m-%Y %H:%M'))

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
            try:
                while True:
                    try:
                        data += connection.recv(1024)
                    except socket.error:
                        break
                sjson = detect_json(data.decode())
                print(sjson)
                if sjson:
                    data = json.loads(sjson)
                    process_save_data_link(data)
                connection.sendall(
                    b'HTTP/1.0 200 OK\r\nContent-Length: 11\r\nContent-Type: text charset=UTF-8\r\n\r\nsuccess\r\n', )
            except Exception:
                connection.sendall(
                    b'HTTP/1.0 200 OK\r\nContent-Length: 11\r\nContent-Type: text charset=UTF-8\r\n\r\nFail\r\n', )
            connection.close()
        except socket.error as err:
            print(err)
