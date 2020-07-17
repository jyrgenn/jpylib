My Python Library
=================

This is meant to be a library package of things I want to have at
hand for my own daily python programming. It shall include all the
things I have developed and want to re-use — modules, utility
functions, and things.

I want to make a PyPi package out of this, such that I can access it
from everywhere (just like pgetopt now) and import into programs as
a whole. That could look like this:

    import jpylib as y

    # trace calls of this function
    @y.fntrace
    def foo(bar, moo=None):
        pass

    ovc, args = y.pgetopts({
        "v": (...),
    })

The two functions called above, `fntrace` and `pgetopts` (which
actually would be `pgetopt.parse`) are indeed the first two I have
in mind.


Current Status
--------------

* `fntrace` — function call tracing decorator.

* `pgetopt` — a submodule `pgetopt` as used elsewhere.

* `kvs` — simple key-value string parser.

* `alerts` – print messages depending on an alert level.

* `namespace` — a value container class with **kwargs initialisation
  and things.

* `config` — reading configuration values from files in Python
  syntax and strings in a simple `key=value` syntax.

* `getsecret` — read a secret from a secrets file

* `sanesighandler` — a decorator to handle SIGINT and SIGPIPE
  signals (or rather the corresponding KeyboardInterrupt and
  BrokenPipeError exceptions) as they should be.

* `terminal_size` — return `columns, rows` of terminal (or `None,
  None` if not available)

* `program`, `home`, `real_home` — basename of `argv[0]`, `$HOME`,
  and the uid's home dir as variables


To Do Next
----------

* testing

* maybe some directory hierarchy traversing support (the need to do
  that comes up again and again)



[ni 2020-07-02] started
