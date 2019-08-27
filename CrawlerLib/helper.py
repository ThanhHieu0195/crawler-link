import functools
import sys
import re
import time


def get_master_attr(key_dot, options, default=None):
    c = options
    for k in key_dot.split('.'):
        if k in c:
            c = c[k]
        elif re.match(r'[0-9]+', k) and type(c) == type([]):
            k = int(k)
            if k < len(c):
                c = c[k]
            else:
                c = default
                break
        else:
            c=default
            break
    return c


def get_sys_params():
    params = {}
    for argv in sys.argv:
        a = str(argv).split('=')
        if len(a) >= 2:
            params[a[0]] = a[1]
    return params


def get_time_log():
    return time.strftime('%d-%m-%Y %H:%I')