import socket
from CrawlerLib.socketjson import _send
from Configs.enum import ServerConfig

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (ServerConfig.IP_ADDRESS.value, ServerConfig.PORT.value)
client.connect(server_address)
_send(client, {
    "action": "assign",
    "params": {
        "id": "100003803082906_1509228895880532",
        "type": "fb"
    }
})
