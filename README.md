
My Python Library
=================

This is meant to be a library package of things I want to have at
hand for my own daily python programming. It shall include all the
things I have developed and want to re-use, modules, utility
functions, and things.

I want to make a PyPi package out of this, such that I can access it
from everywhere (just like pgetopt now) and import into programs as
a whole. That could look like this:

    import tools_jyrgenn as y

    # trace calls of this function
    @y.fntrace
    def foo(bar, moo=None):
        pass

    ovc, args = y.pgetopt({
        "v": (...),
    })

The two functions called above, `fntrace` and `pgetopt` (which
actually would be `pgetopt.parse`) are indeed the first two I have
in mind.


Current Status
--------------

* `fntrace` — function call tracing decorator

* `pgetopt` — a submodule `pgetopt` as used elsewhere.

* `kvs` — simple key-value string parser

* the "print depending on verbosity" functions, with logging

* `namespace` — a value container class with **kwargs initialisation
  and things

* the configuration mechanism as in run-jobs


Planned Items
-------------

* 


[ni 2020-07-02] started
