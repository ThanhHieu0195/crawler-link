import socket
from CrawlerLib.socketjson import _send
from Configs.enum import ServerConfig

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (ServerConfig.IPADDRESS.value, ServerConfig.PORT.value)
client.connect(server_address)
_send(client, {"action": "assign", "addr": "172.17.0.3"})