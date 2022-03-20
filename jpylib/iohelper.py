# Part of jpylib: read lines/items from one or more files. Skip empty and
# commented lines (matching /^\s*#/), strip leading and trailing blanks.

import os
import sys
import re
from .assorted import identity

def all_input_lines(fnames=[], cont_err=False):
    """Like Perl's diamond operator <>, return lines from files or stdin.

    (Generator) If fnames is empty, return lines from stdin, otherwise
    lines from the named files, in succession. The file name "-" stands
    for stdin. Typically, something like sys.argv[1:] would be passed
    as an argument. If cont_err is true, continue after an error,
    printing an error message. If cont_err is a callable, call it with
    the file name and the exception on error.
    """
    # The following looks like a needless duplication of code. But in the
    # spirit of "it is more important for the interface to be simple than the
    # implementation", it must be like this. Factoring out the reading or the
    # exception handling would make the resulting exception stack more
    # complicated, which I want to avoid. Also, I want it to read stdin from
    # sys.stdin so I can easier redirect the input for testing.
    if not fnames:
        fnames = ["-"]
    for fname in fnames:
        try:
            if fname == "-":
                for line in sys.stdin:
                    yield line
            else:
                with open(fname) as f:
                    for line in f:
                        yield line
        except Exception as e:
            if cont_err:
                if callable(cont_err):
                    cont_err(fname, e)
                else:
                    program = os.path.basename(sys.argv[0])
                    print(program+":", e, file=sys.stderr)
            else:
                raise e


def read_items(fname, lstrip=True, rstrip=True, comments_re="^\\s*#",
               skip_empty=True, skip_comments=True, cont_err=False):
    
    """Read lines/items from one or more files (generator).

    With the defaults, comment ("# ...") and empty lines are skipped, and
    whitespace is stripped from the left and right ends of each line.

    `fname` is the name of the file to read; "-" may be used for stdin.

    If `lstrip` is True, whitespace will be stripped from the left side of
    each line. If it is a string, it specifies the characters to be stripped.

    If `rstrip` is True, whitespace will be stripped from the right side of
    each line. If it is a string, it specifies the characters to be stripped.

    `comments_re` is used to match comment lines to be skipped (after the
    stripping of whitespace or other characterns is done). If it is false,
    no comment lines will be stripped.

    If `skip_empty` is true, lines that are empty after the stripping of
    whitespace (or what else is specified) are skipped.

    If `cont_err` is true, continue after a file open or read error, printing
    an error message. If `cont_err` is a callable, call it with the file name
    and the exception on error.

    """
    def lstrip_func(chars):
        """Return function to strip chars from the left siide of a string."""
        def lstrip_f(s):
            return s.lstrip(chars)

    def rstrip_func(chars):
        """Return function to strip chars from the right side of a string."""
        def rstrip_f(s):
            return s.rstrip(chars)

    if lstrip:
        if isinstance(lstrip, str):
            lstripper = lstrip_func(lstrip)
        else:
            lstripper = str.lstrip
    else:
        lstripper = identity

    if rstrip:
        if isinstance(rstrip, str):
            rstripper = rstrip_func(rstrip)
        else:
            rstripper = str.rstrip
    else:
        rstripper = identity

    if comments_re:
        skip_re = re.compile(comments_re)
    else:
        skip_re = False

    for line in all_input_lines((fname,), cont_err=cont_err):
        line = rstripper(lstripper(line))
        if skip_empty and not line:
            continue
        if skip_re and skip_re.search(line):
            continue
        yield(line)

# EOF
