#!/usr/bin/env python3

from jpylib import is_trace, trace, alert_level, L_TRACE

def tracefn(func):
    """Decorator: trace decorated function if trace level is set."""
    def wrapper(*args, **kwargs):
        if is_trace():
            s = "call {}({}".format(func.__name__, ', '.join(map(repr, args)))
            if kwargs:
                for k, v in kwargs.items():
                    s += ", {}={}".format(k, repr(v))
            trace(s + ")")
        return func(*args, **kwargs)
    return wrapper

