import os, sys
from CrawlerLib.helper import get_sys_params, get_time_log

if sys.platform.lower() == "win32":
    os.system('color')


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


def show_text(msg):
    print(msg)


def show_warning(msg):
    if 'debug' in params:
        print(style.BLUE(msg) + style.RESET(""))
    else:
        print('[%s Error] %s' % (get_time_log(), msg))


def show_notify(msg):
    if 'debug' in params:
        print(style.BLUE(msg) + style.RESET(""))
    else:
        print('[%s Notify] %s' % (get_time_log(), msg))


def show_debug(msg):
    if 'debug' in params:
        print(style.YELLOW(msg) + style.RESET(""))
    else:
        print('[%s Debug] %s' % (get_time_log(), msg))
