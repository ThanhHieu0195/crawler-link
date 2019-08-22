from enum import Enum
import os

class ServerConfig(Enum):
    IPADDRESS = os.getenv('IPADDRESS', '172.17.0.2')
    PORT = os.getenv('PORT', 12345)
    NUMCLIENT=os.getenv('NUMCLIENT', 5)
