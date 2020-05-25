#!/usr/bin/env python3
# test: trigger assertion 2

import pgetopt

ovc, args = pgetopt.parse({
    "v": (b"verbose", bool, 0, "increase verbosity"),
})
