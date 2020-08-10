#!/usr/bin/env python3

# Resolve #include statements similar to the C preprocessor, print result to
# stdout.
#
# The #include must be at the beginning of the line, no blanks. Include files
# may be nested, but the nesting depth is limited by the number of available
# file descriptors.
#
# If the include argument starts with an exclamation mark, treat the argument as
# a shell command line, whose output shall be included.

import os
import sys
import jpylib as y

had_error = 0
stdin_fname = "/dev/stdin"

def do_fd(fd, fname=stdin_fname):
    """Process a file given by fd."""
    lineno = 0
    for line in fd:
        lineno += 1
        if line.startswith("#include"):
            try:
                argument = line.split(" ", 1)[1].strip()
                if argument.startswith("!"):
                    do_command(argument[1:], fname)
                else:
                    do_fname(argument)
            except Exception as e:
                global had_error
                had_error = True
                print("%s:%d: %s" % (fname, lineno, e), file=sys.stderr)
        else:
            print(line, end="")
    

def do_command(command, source):
    """Run command and print it to stdout.

    Make sure the included text is terminated by a newline. Set the SOURCE
    environment variable to the file from which the "#include !..." command is
    currently being processed. This may be a file included by another.

    """
    os.environ["SOURCE"] = source
    output = y.backquote(command)
    if output.endswith("\n"):
        terminate = ""
    else:
        terminate = "\n"
    print(output, end=terminate)


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
