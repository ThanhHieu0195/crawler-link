import socket
from CrawlerLib.socketjson import _send, _recev
from Configs.enum import ServerConfig

idx = 1
def assign_task(data):
    global idx
    master_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (ServerConfig.IP_ADDRESS.value, ServerConfig.PORT.value)
    master_client.connect(server_address)

    print(idx, 'run task: ', data['link_id'])
    idx = idx + 1
    _send(master_client, {
        "action": "assign",
        "params": data
    })
    _recev(master_client)
    master_client.close()
