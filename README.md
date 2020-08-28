My Python Library
=================

This is meant to be a library package of things I want to have at
hand for my own daily python programming. It shall include all the
things I have developed and want to re-use — modules, small utility
functions, and things.

This is a PyPi package so I can access it from everywhere and import
it into programs as a whole. That could look like this:

    import jpylib as y

    # trace calls of this function
    @y.tracefn
    def foo(bar, moo=None):
        pass

    ovc, args = y.pgetopts({
        "v": (...),
    })

The two functions called above, the `tracefn` decorator and
`pgetopts` were indeed the first two I had in mind. Quite a few more
followed in between.


Components
----------

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

* `outputCaptured`, `outputAndExitCaptured` – context managers to
  capture the output and/or system exit status of some code.

* `backquote` — get the output of an external command as simple as
  with the Perl backquote construct.

* `boolish` — a function to make bool values from strings like
  "yes", "no", "on", "off", etc. that are potentially used in
  interactive answers and some config files.

* `flatten` — generator, flatten a sequence (except strings)


Documentation
-------------

Real documentation is still to be written for most things. For now,
refer to the source code, in particular to the function docstrings.

This is what is already there:

* [pgetopt](doc/pgetopt.md)


To Do Next
----------

* real documentation

* maybe some directory hierarchy traversing support (the need to do
  that comes up again and again)

* table formatting

[ni 2020-07-02] started
