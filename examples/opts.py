#!/usr/bin/env python3

import jpylib as y

ovc, args = y.pgetopts({
    "_arguments": ["arg1"],
    "_help_header": "Demonstrate options descriptor usage.",
    "_help_footer": "For any questions, please consult the documentation.",
    "q": ("quiet", y.alert_level_zero, y.alert_level(y.L_NOTICE),
          "be quiet (no output except error messages)"),
    "v": ("verbose", y.alert_level_up, y.alert_level(y.L_NOTICE),
          "increase verbosity (up to 3 make sense)"),
    "n": ("number", int, 0, "set a number value"),
    "s": ("string", str, None, "a string option", "STRING-OPTION"),
    "x": ("flag", bool, False, "an arbitrary flag value"),
})

print("Option values:", ", ".join([
    f"{key}={repr(value)}" for key, value in ovc.ovc_values().items() ]))
print()
y.trace("a trace message")
y.debug("a debug message")
y.info("an info message")
y.notice("a notice message")
y.err("an error message")
y.fatal("a fatal error message ended the program")

