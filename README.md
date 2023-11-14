My Python Library
=================

`jpylib` is a library package of things I want to have at hand for
my own daily Python programming. It includes a number of programming
utilities I have developed and want to re-use.

This is a PyPi package, named `jpylib-jyrgenn` so I can access it
from everywhere as <https://pypi.org/project/jpylib-jyrgenn/> and
import it into programs as a whole. That could look like this:

    import jpylib as y

    # trace calls of this function
    @y.tracefn
    def foo(bar, moo=None):
        pass

    ovc, args = y.pgetopts({
        "v": (...),
    })

The two functions called above, the `tracefn` decorator and the
`pgetopts()` function were indeed the first two I had in mind. Quite
a few more followed in between.


Components
----------

See the documentation (referenced below) for a list of the
components.

Documentation
-------------

* [jpylib](doc/jpylib.md): brief documentation of the jpylib
  functionality.

* [pgetopts](doc/pgetopts.md): somewhat more extensive documentation
  of the `pgetopts()` function, the library's most complex component


To Do Next
----------

* maybe some directory hierarchy traversing support (the need to do
  that comes up again and again)

[ni 2022-08-13] started
