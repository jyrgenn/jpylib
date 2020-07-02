#!/usr/bin/env python3


def fntrace(func):
    def wrapper(*args, **kwargs):
        print(f"call {func.__name__}({', '.join(map(repr, args))}", end="")
        if kwargs:
            for k, v in kwargs.items():
                print(f", {k}={repr(v)}", end="")
        print(")")
        return func(*args, **kwargs)
    return wrapper

@fntrace
def this_function(start, end, step=1):
    hadone = False
    print(f"i am func({repr(start)}, {repr(end)}, {repr(step)})")
    for i in range(start, end, step):
        hadone = True
        print(f"{i} ", end="")
    if hadone:
        print()


print("Hoolalah")

this_function(2, 35, step=2)
this_function(1, 5)
