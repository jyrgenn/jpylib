#!/usr/bin/env python3

import pgetopt

ovc, args = pgetopt.parse({
    "s": ("schmooze", bool, 0, "increase schmooziness"),
    "o": ("output_file", str, None, "output file (or stdout)", "NAME"),
    "n": ("repetitions", int, 3, "number of repetitions"),
    "d": ("debug", str, [], "debug topics", "DEBUG_TOPIC"),
    "_arguments": ("string_to_print", "[...]"),
    "_help_header": "print a string a number of times",
    "_help_footer": "This is just an example program.",
}, exit_on_error=True)
print(ovc)
print(ovc._values(), args)
