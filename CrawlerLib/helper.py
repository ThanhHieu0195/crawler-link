import functools
import re


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
