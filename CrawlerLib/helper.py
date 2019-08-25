import functools

raise_attribute_error = object()
def nested_getattr(obj, attr, default=raise_attribute_error):
    try:
        return functools.reduce(getattr, attr.split('.'), obj)
    except AttributeError:
        if default != raise_attribute_error:
            return default
        raise