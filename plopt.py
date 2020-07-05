#!/usr/bin/env python3

import pylib as y

ovc, args = y.pgetopts({
    "v": ("verbose", y.print_level_up, y.print_level(), "increase verbosity"),
    "l": ("locals", locals, None, "the local vars"),
    "q": ("quiet", y.print_level_zero, False, "be quiet"),
})

@y.fntrace
def fun_fun_fun(a, b, add=3):
    return (a + b) + add

print(ovc.ovc_values())
print(fun_fun_fun(5, 6))
print(fun_fun_fun(5, 6, 7))
print(fun_fun_fun(5, 6, add=8))

