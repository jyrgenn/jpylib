#!/usr/bin/env python3

import jpylib as y

y.print_level(y.L_TRACE)

ovc, args = y.pgetopts({
    "v": ("verbose", y.print_level_up, y.print_level(), "increase verbosity"),
    "l": ("locals", locals, None, "the local vars"),
    "g": ("globals", globals, None, "the global vars"),
    "q": ("quiet", y.print_level_zero, False, "be quiet"),
})

@y.fntrace
def fun_fun_fun(a, b, add=3):
    return (a + b) + add

print(ovc.ovc_values())
print(fun_fun_fun(5, 6))
print(fun_fun_fun(5, 6, 7))
print(fun_fun_fun(5, 6, add=8))
print()

print(y.parse_kvs("karl=frits,schum={sigs=[1,2,15],3=4},moo=0",
                  intvals=True))
print(y.parse_kvs("foo=bar,dang=[1,2,15],d={a=b,c=[d,e,f],quux=blech},e=not",
                  intvals=True))

ns = y.Namespace(foo="hanselmann", bar=3, singer=[15,2,3,8,9])
print(ns)
print(repr(ns))

