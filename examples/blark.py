#!/usr/bin/env python3

import jpylib as y

ovc, args = y.pgetopts({
    "v": ("verbose", bool, False, "be verbose"),
    "o": ("output_file", str, "/dev/stdout", "output file", "PATHNAME"),
    "i": ("iterations", int, 1, "number of iterations"),
    "_arguments": ["gnumm", "..."],
})

if ovc.verbose:
    print(ovc.ovc_values())
print("args:", args)
