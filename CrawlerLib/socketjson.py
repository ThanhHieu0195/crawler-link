import json
import pprint
import socket

from CrawlerLib.show_notify import show_debug, show_warning


def _send(s, data):
    try:
        msg = json.dumps(data).encode()
    except Exception as e:
        show_warning(format(e))
        msg = b''
    s.send(msg)


def _recev(s, default={}):
    data = default
    try:
        msg = s.recv(10240)
        data = json.loads(msg.decode())
    except json.JSONDecodeError as e1:
        print(e1)
        data = {}
    except socket.error as e:
        show_warning(format(e))
    return data
