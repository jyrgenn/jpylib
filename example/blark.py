#!/usr/bin/env python3

import pgetopt

ovc, args = pgetopt.parse({
    "v": ("verbose", bool, False, "be verbose"),
    "o": ("output_file", str, "/dev/stdout", "output file"),
    "i": ("iterations", int, 1, "number of iterations"),
    "_arguments": ("gnumm", "braller", "..."),
})

if ovc.verbose:
    print(ovc.ovc_values())
print("args:", args)
