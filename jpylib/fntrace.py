#!/usr/bin/env python3

from .print_level import is_trace, trace, print_level, L_TRACE

def fntrace(func):
    """Decorator: trace decorated function if trace level is set."""
    def wrapper(*args, **kwargs):
        if is_trace():
            s = f"call {func.__name__}({', '.join(map(repr, args))}"
            if kwargs:
                for k, v in kwargs.items():
                    s += f", {k}={repr(v)}"
            trace(s + ")")
        return func(*args, **kwargs)
    return wrapper


if __name__ == "__main__":

    print_level(L_TRACE)

    @fntrace
    def this_function(start, end, step=1):
        hadone = False
        print(f"=> i am func({repr(start)}, {repr(end)}, {repr(step)})")
        for i in range(start, end, step):
            hadone = True
            print(f"{i} ", end="")
        if hadone:
            print()


    print("Hoolalah")

    this_function(2, 35, step=2)
    this_function(1, 5)
