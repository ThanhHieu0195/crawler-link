import json


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
