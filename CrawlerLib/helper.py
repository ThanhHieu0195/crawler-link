import functools
import re
from CrawlerLib.show_notify import show_debug

raise_attribute_error = object()
def nested_getattr(obj, attr, default=raise_attribute_error):
    try:
        return functools.reduce(getattr, attr.split('.'), obj)
    except AttributeError:
        if default != raise_attribute_error:
            return default
        raise


def get_master_attr(key_dot, options, default=None):
    c = options
    for k in key_dot.split('.'):
        print(k)
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
