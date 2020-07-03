# print functions depending on a verbosity level

import os
import sys

_verbose_print_level = 1

_verbose_print_decoration = [
    "ERROR",
    None,
    None,
    "DBG",
    "TRC",
]
_verbose_print_max_level = len(_verbose_print_decoration)

_verbose_print_level_fds = [
    sys.stderr,
    sys.stderr,
    sys.stderr,
    sys.stderr,
    sys.stderr,
]

_verbose_print_program = os.path.basename(sys.argv[0])

_verbose_print_use_syslog = False


def verbose_print_config(*, level=None, program=None, level_fds=None,
                         use_syslog=False, _):
    if level is not None:
        verbose_print_level(level)
    if program is not None:
        _verbose_print_program = program
    if level_fds is not None:
        _verbose_print_level_fds = level_fds
    if use_syslog is not None:
        _verbose_print_use_syslog = use_syslog


def verbose_print_level_config(level, *, fd=None, decoration=None):
    assert 0 <= level <= _verbose_print_max_level, \
        "level value not between 0 and " + str(verbose_print_max_level)
    if fd is not None:
        _verbose_print_level_fd[level]
    if decoration is not None:
        _verbose_print_decoration[level] = decoration


def verbose_print_level(level=None):
    """Get or set the verbosity level for the verbosity-print functions.

    err() will print something with level 0 (and greater).
    notice() will print something with level 1 (and greater).
    info() will print something with level 2 (and greater).
    debug() will print something with level 3 (and greater).
    trace() will print something with level 4 (and greater).
    """
    global _verbose_print_level
    if level is not None:
        _verbose_print_level = max(0, min(level, _verbose_print_max_level))
    return _verbose_print_level


def _verbose_print(level, *msgs):
    """Print a message if `level` is <= the _verbose_print_level.

    If a decoration exists in `_verbose_print_decoration[]` for that level, is it
    prepended to the message. By default, all levels print to stderr; this can
    be changed in `_verbose_print_level_fds[]` by level.

    """
    msgs = list(map(str, msgs))
    if _verbose_print_decoration[level]:
        msgs = _verbose_print_decoration[level]
    if level <= _verbose_print_level:
        print(_verbose_print_program+":", *msgs,
              file=_verbose_print_level_fds[level])
    if _verbose_print_use_syslog:
        if not syslog_opened:
            syslog.openlog(logoption=syslog.LOG_PID, facility=syslog.LOG_MAIL)
        level = max(0, min(len(verb_print_decoration) - 1, level))
        message = " ".join(map(str, msgs))
        syslog.syslog(syslog_prio[level], message)


def err(*msg):
    _verbose_print(0, "ERROR", *msg)

def notice(*msg):
    _verbose_print(1, *msg)

def info(*msg):
    _verbose_print(2, *msg)

def debug(*msg):
    _verbose_print(3, "DBG", *msg)
