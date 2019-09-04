import socket
from CrawlerLib.socketjson import _send, _recev
from Configs.enum import ServerConfig

master_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (ServerConfig.IP_ADDRESS.value, ServerConfig.PORT.value)
master_client.connect(server_address)


def assign_task(data):
    print('run task: ', data)
    _send(master_client, {
        "action": "assign",
        "params": data
    })
    _recev(master_client)
