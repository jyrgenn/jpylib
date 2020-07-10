#!/usr/bin/env python3
# test: trigger assertion 3

import jpylib as y

ovc, args = y.pgetopts({
    "v": ("verbose", float, 0, "increase verbosity"),
})
