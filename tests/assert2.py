#!/usr/bin/env python3
# test: trigger assertion 2

import jpylib as y

ovc, args = y.pgetopts({
    "v": (b"verbose", bool, 0, "increase verbosity"),
})
