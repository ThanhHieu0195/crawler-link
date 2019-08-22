import json


def _send(socket, data):
    try:
        msg = json.dumps(data).encode()
    except:
        msg = ''
    socket.send(msg)


def _recev(socket):
    try:
        data = json.loads(socket.recv(1024))
    except:
        data = {}
    return data
