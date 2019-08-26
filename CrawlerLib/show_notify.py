import os, sys
import logging
from CrawlerLib.helper import get_sys_params, get_master_attr

if sys.platform.lower() == "win32":
    os.system('color')

# Group of Different functions for different styles
class style():
    BLACK = lambda x: '\033[30m' + str(x)
    RED = lambda x: '\033[31m' + str(x)
    GREEN = lambda x: '\033[32m' + str(x)
    YELLOW = lambda x: '\033[33m' + str(x)
    BLUE = lambda x: '\033[34m' + str(x)
    MAGENTA = lambda x: '\033[35m' + str(x)
    CYAN = lambda x: '\033[36m' + str(x)
    WHITE = lambda x: '\033[37m' + str(x)
    UNDERLINE = lambda x: '\033[4m' + str(x)
    RESET = lambda x: '\033[0m' + str(x)


params = get_sys_params()
log_name = get_master_attr('log_name', params, 'log.log')
path_log='%s/Log/%s' % (os.getcwd(), log_name)
print(path_log)
logging.basicConfig(filename=path_log, level=logging.DEBUG)

def show_warning(msg):
    if 'debug' in params:
        print(style.BLUE(msg) + style.RESET(""))
    else:
        print('[Error] %s' % msg)
        logging.warning(msg)


def show_info(msg):
    if 'debug' in params:
        print(style.BLUE(msg) + style.RESET(""))
    else:
        print('[Notify] %s' % msg)
        logging.info(msg)

def show_debug(msg):
    if 'debug' in params:
        print(style.YELLOW(msg) + style.RESET(""))
    else:
        print('[Debug]: %s' % msg)
        logging.debug(msg)