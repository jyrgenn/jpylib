#!/usr/bin/env python3

# Resolve #include statements similar to the C preprocessor, print result to
# stdout. The #include must be at the beginning of the line, no blanks. Include
# files may be nested, but the nesting depth is limited by the number of
# available file descriptors.

import sys

had_error = 0

def do_fd(fd, fname="<stdin>"):
    """Process a file given by fd."""
    lineno = 0
    for line in fd:
        lineno += 1
        if line.startswith("#include"):
            try:
                do_fname(line.split(" ", 1)[1].strip())
            except Exception as e:
                global had_error
                had_error = True
                print(f"{fname}:{lineno}: {e}", file=sys.stderr)
        else:
            print(line, end="")
    

def do_fname(fname):
    """Process a file specified by name."""
    with open(fname) as fd:
        do_fd(fd, fname)


if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        do_fname(arg)
else:
    do_fd(sys.stdin)

sys.exit(had_error)
