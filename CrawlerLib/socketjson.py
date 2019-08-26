import json
import pprint

from CrawlerLib.show_notify import show_debug


def _send(socket, data):
    try:
        msg = json.dumps(data).encode()
    except:
        msg = ''
    socket.send(msg)


def _recev(socket):
    try:
        msg = socket.recv(10240)
        data = json.loads(msg.decode())
    except:
        data = {}
    return data
