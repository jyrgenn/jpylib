#!/usr/bin/env python3

# generate option description table for the README
# usage: $0 file

import sys

# widths are at least those of the header fields
widths = [len("Constant"), len("Message"), len("Argument")]

lines = []

with open(sys.argv[1]) as f:
    for line in f:
        if line.startswith("Error"):
            elems = [0, 0, 0]
            elems[0], rest = line.split("=")
            elems[1], elems[2] = rest.split("#")
            for i, el in enumerate(elems):
                elems[i] = el.strip()
                widths[i] = max(widths[i], len(elems[i]))
            elems[0] = f"`{elems[0]}`"
            lines.append(elems)

for line in lines:
    # the nice thing about Python's string formatting methods is that there are
    # so many of them to choose from
    print(("| {:%d} | {:%d} | {:%d} |" % tuple(widths)).format(*line))
