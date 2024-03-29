#!/usr/bin/env python3
# pgetopts example program [ni@w21.org 2020-05-22]

import sys
import jpylib as y

ovc, args = y.pgetopts({
    # opt: (name,        type, default value, helptext[, arg name])
    "s": ("schmooze",    bool, 0,    "more schmooziness"),
    "o": ("output_file", str,  None, "output file (or stdout)", "NAME"),
    "n": ("repetitions", int,  3,    "number of repetitions"),
    "d": ("debug",       str, [],    "debug topics", "DEBUG_TOPIC"),
    # keyword:        value
    "_arguments":   ["string_to_print", "..."],
    "_help_header": "print a string a number of times",
    "_help_footer": "This is just an example program.",
})

if ovc.output_file:
    out = open(ovc.output_file, "w")
else:
    out = sys.stdout

if ovc.debug:
    print("debug", *ovc.debug, file=sys.stderr)

for i in range(ovc.repetitions):
    for i in range(ovc.schmooze):
        print("schmooze ", end="", file=out)
    print(*args, file=out)

# EOF
