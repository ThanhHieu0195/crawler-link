import socket


def create_server(address, port, num_client=5):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (address, port)
    print('starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)
    sock.listen(num_client)
    return sock


def get_master_option(options):
    if len(options) > 0:
        current = None
        for o in options:
            if o['status'] is True:
                if current is None:
                    current = o
                elif o['amount'] > current['amount']:
                    current = o
        if current is not None:
            return current
    return None
