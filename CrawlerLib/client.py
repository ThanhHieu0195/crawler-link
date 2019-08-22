import socket

def create_client(address, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (address, port)
    client.connect(server_address)
    return client