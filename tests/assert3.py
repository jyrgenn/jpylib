#!/usr/bin/env python3
# test: trigger assertion 3

import pgetopt

ovc, args = pgetopt.parse({
    "v": ("verbose", float, 0, "increase verbosity"),
})
