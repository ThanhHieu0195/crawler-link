import socket
from CrawlerLib.socketjson import _send
from Configs.enum import ServerConfig

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (ServerConfig.IP_ADDRESS.value, ServerConfig.PORT.value)
client.connect(server_address)


def assign_task(data):
    _send(client, {
        "action": "assign",
        "params": data
    })

