#!/usr/bin/env python3
# just try out some of those functions

import time
import jpylib as y

y.print_level(y.L_TRACE)

ovc, args = y.pgetopts({
    "v": ("verbose", y.print_level_up, y.print_level(), "increase verbosity"),
    "l": ("locals", locals, None, "the local vars"),
    "g": ("globals", globals, None, "the global vars"),
    "q": ("quiet", y.print_level_zero, False, "be quiet"),
    "c": ("config_file", str, None, "configuration file path"),
    "C": ("config_item", str, [], "configuration item(s)"),
})

@y.fntrace
def fun_fun_fun(a, b, add=3):
    return (a + b) + add

@y.sanesighandler
def nap():
    """sleep a bit, so we can interrupt"""
    print("interrupt now?")
    time.sleep(3)

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
print(ns.foo)
print(repr(ns))
print()

cfg = y.Config(
    owner = "jni",
    permissions = 0o751,
    signals = [15, 15, 15, 15, 2, 2, 2, 3, 3, 3, 6, 6, 6, 9, 9, 9, 9, 9,],
    dirs = {
        "lib": "/usr/local/lib",
        "bin": "/usr/local/bin",
    },
    err_exit = 2,
)
if ovc.config_file:
    cfg.load_from(ovc.config_file)
if ovc.config_item:
    for item in ovc.config_item:
        cfg.update_from_string(item)
print(cfg)
nap()

print("getsecret test: ", end="")
y.getsecret_main()
