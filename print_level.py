# print functions depending on a verbosity level

import os
import sys
import inspect

print_level_name = [
    "L_ERROR",
    "L_NOTICE",
    "L_INFO",
    "L_DEBUG",
    "L_TRACE",
]
for i, name in enumerate(print_level_name):
    locals()[name] = i
print_max_level = len(print_level_name) - 1

print_level_level = 1

print_level_decoration = [
    "ERROR",
    None,
    None,
    "DBG",
    "TRC",
]

print_level_fds = [
    sys.stderr,
    sys.stderr,
    sys.stderr,
    sys.stderr,
    sys.stderr,
]


print_level_program = os.path.basename(sys.argv[0])

print_level_use_syslog = False

had_errors = False


def print_level_config(*, level=None, program=None, level_fds=None,
                         use_syslog=False, _):
    if level is not None:
        print_level(level)
    if program is not None:
        print_level_program = program
    if level_fds is not None:
        print_level_fds = level_fds
    if use_syslog is not None:
        print_level_use_syslog = use_syslog


def print_level(level=None):
    """Get or set the verbosity level for the verbosity-print functions.

    err() will print something with level 0 (and greater).
    notice() will print something with level 1 (and greater).
    info() will print something with level 2 (and greater).
    debug() will print something with level 3 (and greater).
    trace() will print something with level 4 (and greater).
    """
    global print_level_level
        
    if level is not None:
        if type(level) is str:
            level = print_level_map[level]
        print_level_level = max(0, min(level, print_max_level))
    return print_level_level


def is_notice():
    """Return True iff the print level is at least at notice."""
    return print_level_level >= L_NOTICE

def is_info():
    """Return True iff the print level is at least at info."""
    return print_level_level >= L_INFO

def is_debug():
    """Return True iff the print level is at least at debugging."""
    return print_level_level >= L_DEBUG

def is_trace():
    """Return True iff the print level is at least at tracing."""
    return print_level_level >= L_TRACE


def print_if_level(level, *msgs):
    """Print a message if `level` is <= the print_level_level.

    If a decoration exists in `print_level_decoration[]` for that level, is
    it prepended to the message. By default, all levels print to stderr; this
    can be changed in `print_level_fds[]` by level.

    If one of the

    """
    # make all msgs elements strings, calling those that are callable
    for i, elem in enumerate(msgs):
        if callable(elem):
            msgs[i] = elem()
        elif type(elem) is not str:
            msgs[i] = str(elem)
    if print_level_decoration[level]:
        msgs = [print_level_decoration[level], *msgs]

    if level <= print_level_level:
        print(*msgs, file=print_level_fds[level])

    if print_level_use_syslog:
        if not syslog_opened:
            syslog.openlog(logoption=syslog.LOG_PID, facility=syslog.LOG_MAIL)
        level = max(0, min(print_max_level, level))
        message = " ".join(map(str, msgs))
        syslog.syslog(syslog_prio[level], message)


def debug_vars(*vars):
    """Print debug output for the named variables."""
    if print_level_level >= L_DEBUG:
        context = inspect.currentframe().f_back.f_locals
        for var in vars:
            print("VAR {}: {}".format(var, repr(context[var])))


def err(*msgs):
    """Print error level output."""
    had_errors = True
    print_if_level(L_ERROR, *msgs)

def notice(*msgs):
    """Print notice level output if so requested."""
    print_if_level(L_NOTICE, *msgs)

def info(*msgs):
    """Print info level output if so requested."""
    print_if_level(L_INFO, *msgs)

def debug(*msgs):
    """Print debug level output if so requested."""
    print_if_level(L_DEBUG, *msgs)

def trace(*msgs):
    """Print debug level output if so requested."""
    print_if_level(L_TRACE, *msgs)

