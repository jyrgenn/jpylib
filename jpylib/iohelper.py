import os
import sys

def all_input_lines(fnames, cont_err=False):
    """Like Perl's diamond operator <>, return lines from files or stdin.

    (Generator) If fnames is empty, return lines from stdin, otherwise
    lines from the named files, in succession. The file name "-" stands
    for stdin. Typically, something like sys.argv[1:] would be passed
    as an argument. If cont_err is true, continue after an error,
    printing an error message. If cont_err is a callable, call it with
    the file name and the exception on error.
    """
    if not fnames:
        fnames = ["/dev/stdin"]
    for fname in fnames:
        if fname == "-":
            fname = "/dev/stdin"
        try:
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
