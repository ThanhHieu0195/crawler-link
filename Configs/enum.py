from enum import Enum
import os


class ServerConfig(Enum):
    IP_ADDRESS = os.getenv('IP_ADDRESS', '172.17.0.2')
    PORT = os.getenv('PORT', 12345)
    NUM_CLIENT = os.getenv('NUM_CLIENT', 5)
    CLIENT_TYPE = os.getenv('CLIENT_TYPE', '')
