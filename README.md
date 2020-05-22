[_this is still work in progress_]

pgetopt module — POSIX-conformant command-line option parser (plus
long options)


Motivation
----------

I wrote this not because there wasn't an option parser available for
Python — I know there are a few — but because I didn't like those
I saw. Argparse, Optparse, Click, they all do more than I need, and
because they do, thay are at the same time cumbersome to use.

What I want is a really simple user interface, one that makes simple
things simple. I don't want to automate sophisticated argument
verification in an option parser. I want it to parse the options,
with potential arguments, and maybe even count the remaining
arguments to be able to throw an error for missing or surplus ones
right there, and to generate a brief usage or detailed help message.

I also want it to be POSIX conformant, because that is the
traditional Unix style.


POSIX Conformance[1]
--------------------

POSIX-conformance means, (single-letter) options can be clustered;
also, the argument of a single-letter option (if it takes one) may
be placed in the next argv[] element, or in the same one, meaning
that after an option letter that needs and argument, the rest of
that argv[] element is the argument, not more clustered options. In
other words, the whitespace separating option and argument is
optional. Thus, `-o foo` and `-ofoo` are equivalent.

But mainly, option parsing stops when the first argv[] element is
encountered that is neither an option or an option argument, i.e. a
regular argument. Example:

    blark -v -o /tmp/blark.out -i 3 gnuddle fuddle -a ruddle

Here, `-v` is an option, `-o` and `-i` are options with an argument,
and `gnuddle` is the first regular argument. Option parsing stops
here, and starting with `gnuddle` all other arguments are considered
regular arguments, including `-a`. This is mandated by POSIX, and
this is where Argparse, Optparse, and Click all fall short.

(Option parsing also stops when a `--` argument is found, which can
be useful if a regular argument follows that starts with a `-`.)

[1] The Open Group Base Specifications Issue 7, 2018 edition
    IEEE Std 1003.1-2017
    https://pubs.opengroup.org/onlinepubs/9699919799/


Usage
-----

One of the main goals was simplicity and brevity of the user
interface. That implies, to some degree, a limitation of what the
option parsing will do, but I found the right balance that feels
right to me. To specify and parse the options of the hypothetical
`blark` program used as example above, all we need is this:

    ovc, args = pgetopt.parse({
        "v": ("verbose", bool, False, "be verbose"),
        "o": ("output_file", str, "/dev/stdout", "output file", "PATHNAME"),
        "i": ("iterations", int, 1, "number of iterations"),
        "_arguments": ("gnumm", "..."),
    })

The parse() function has, in the usual case, one argument, a
dictionary describing the options. The one-letter strings as keys
are the option letters; their values are the option descriptors,
tuples or lists of four or five elements. These are:

1. the name of the option in the namespace returned, also (with `_`
   replaced by `-`) the name of the corresponding long option
2. the type: `bool` (boolean, actually a counter), `str` (needs
   argument), `int` (needs integer argument)
3. the default value (or counter start in case of bool); it may be
   a list collecting the arguments of multiple occurrances of the
   option
4. the text for the help output
5. [optional] a placeholder for the argument

IMO these descriptors with 4 or at most 5 elements is short enough
to use positional parameters without sacrificing clarity or ease of
use. So, as there are no named parameters, there is little clutter,
keeping the whole thing short and easy to read.


Then, there may be a few key/value pairs where the key is a keyword:

`_arguments`
: either a string describing the command's arguments, or a tuple or
list with those. In the latter case, it is used to determine the
minimum and maximum number of arguments. See below at "Argument
count checking" for more information.

`_help_header`
: a string that will be printed at the top of the help message.

`_help_footer`
: a string that will be printed at the bottom of the help message.

The two values returned are an option value container, where the
values can be access with `ovc.verbose`, `ovc.output_file` etc., and
a list with the remaining arguments.

And that is indeed all you need to know. One simple example
exercises nearly all features of this package:

    ovc, args = pgetopt.parse({
        # opt: (name,        type, default value, helptext[, arg name])
        "s": ("schmooze",    bool, 0,    "increase schmooziness"),
        "o": ("output_file", str,  None, "output file (or stdout)", "NAME"),
        "n": ("repetitions", int,  3,    "number of repetitions"),
        "d": ("debug",       str, [],    "debug topics", "DEBUG_TOPIC"),
        # keyword:        value
        "_arguments":   ("string_to_print", "..."),
        "_help_header": "print a string a number of times",
        "_help_footer": "This is just an example program.",
    })

| Field             | Value                                                 |
|-------------------|-------------------------------------------------------|
| `ovc.schmooze`    | the number of `-s` options counted                    |
| `ovc.output_file` | the parameter of `-o` or `--output-file`, or `None`   |
| `ovc.repetitions` | the parameter of `-n` or `--repetitions`, or `3`      |
| `ovc.debug`       | a list with all parameters given to `-d` or `--debug` |

(See the `schmooze.py` program in the `examples/` directory to see
this in the context of a program.)

When the program using this gets called with an invalid option or
the wrong number of arguments (in this case: none), or when it sees
the `-?` or `--usage` option, a corresponding error and a brief
usage message are printed and the program exits with an exit status
of 1. When the program is called with `-h` or `--help`, a more
detailed help message is printed, consisting of the usage, the
`_help_header` value (if present), an explanation of the options
constructed from the option descriptors, and the `_help_footer`
value (if present).


The help and usage messages are available from the option value
container by calling the `ovc_help_msg` and `ovc_usage_msg` methods,
which return the respective message. Or call the `ovc_help` and
`ovc_usage` methods, which print their message and end the program.


Argument count checking
-----------------------

As mentioned above, if the `_arguments` field of the options
descriptor is a list or tuple, the number of actual arguments is
checked against the minimum and maximum number of arguments derived
from this sequence. This is intended to capture the tradition of
Unix command argument synopses and works as follows:

 * Each "normal" string increases the minimum and the maximum by
   one.

 * The string `"..."` sets the maximum to infinity, but does not
   change the minimum.

 * Any other string that contains `...` sets the maximum to
   infinity, but also increases the minimum by one.

 * A string that begins with `[` is split by blanks, and the number
   of its parts increases the maximum, but does not change the
   minimum.

So this means, for example:

 * `("source", "destination")`: minimum = 2, maximum = 2

 * `("file1", "...")`: minimum = 1, maximum none

 * `("file1", "...", "destination")`: minimum = 2, maximum none

 * `("file1...", "destination")`: minimum = 2, maximum none

 * `("arg1", "[arg2]")`: minimum = 1, maximum = 2

 * `("arg1", "[arg2 [arg3 arg4]]")`: minimum = 1, maximum = 4  
   (In this case a number of 3 arguments would be illegal, but there
   is no provision to check for that.)

The latter illustrates how I try to achieve a balance between
simplicity of the interface and the brevity of the code on one side
and the capabilties of this module on the other: Being able to check
for more than a minimum and a maximum number of arguments would
either have made the interface or the implementation more complex,
and given that this is rarely needed, I chose to omit that.


Limitations
-----------

The simple interface and a compact implementation result in a few
limitations.

 * There can be no single-letter option without a logn option and
   vice versa.

 * Checking for errors in the passed option descriptors dictionary
   is rudimentary.

 * Passing an argument to the help option in the same argv[] element
   results in `ovc.help` being set to that value, and not a call to
   the `ovc_help` method.


Examples and Testing
--------------------

The examples above can also be found in the `examples/` directory.

`test.py` is the beginning of a test suite, but it is rather in the
early stages, not to say immature.
