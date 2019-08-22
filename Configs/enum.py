from enum import Enum
import os
from dotenv import load_dotenv
load_dotenv()


class ServerConfig(Enum):
    IP_ADDRESS = os.getenv('IP_ADDRESS', '172.17.0.2')
    PORT = int(os.getenv('PORT', 12345))
    NUM_CLIENT = int(os.getenv('NUM_CLIENT', 5))
    CLIENT_TYPE = os.getenv('CLIENT_TYPE', '')
    MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
    MONGO_PORT = int(os.getenv('MONGO_PORT', '27017'))
