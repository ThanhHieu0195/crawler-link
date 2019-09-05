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
    MONGO_DATABASE = os.getenv('MONGO_DATABASE', 'crawler')
    API_YTB_KEY = os.getenv('API_YTB_KEY', None)
    TIME_OUT=15
    ENABLE_SCREENSHOT=True
    SELENIUM_TYPE=os.getenv('SELENIUM_TYPE', 'firefox')
    SELENIUM_CHROME_DRIVER_PATH=os.getenv('SELENIUM_CHROME_DRIVER_PATH', '/usr/local/bin/chromedriver')
