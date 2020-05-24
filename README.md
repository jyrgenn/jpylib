;; -*- text -*-

pgetopt module
==============

This package implements a command-line option parser. The underlying
idea was to have it POSIX conformant, additionally implement long
options, while striking the right balance between simplicity and
clarity of the user interface, brevity of the code, and the
implemented capabilities.

  * [Motivation](#motivation)
  * [POSIX Conformance[1]](#posix-conformance1)
  * [Usage](#usage)
  * [Argument count checking](#argument-count-checking)
  * [The parse() function](#the-parse-function)
  * [Exceptions](#exceptions)
  * [The OptionValueContainer](#the-optionvaluecontainer)
  * [Limitations](#limitations)
  * [Semi\-hidden feature: option value callbacks](#semi-hidden-feature-option-value-callbacks)
  * [Documentation, Examples and Testing](#documentation-examples-and-testing)
  * [Building the PyPi package](#building-the-pypi-package)


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
right there, and to generate a brief usage or more detailed help
message.

But mainly I want to impose as little obligation as possible on the
calling program — a single function call ought to be all to gain
easy access to the option values.

I also want the option parsing to be POSIX conformant, because that
is the traditional Unix style.


POSIX Conformance[1]
--------------------

POSIX-conformance means, in the context of command-line options,
(single-letter) options can be clustered; also, the argument of a
single-letter option (if it demands one) may be placed in the next
`argv[]` element, or in the same one, meaning that after an option
letter that demands an argument, the rest of that `argv[]` element,
if any, is the option argument, not more clustered options. In other
words, the whitespace separating option and argument is optional.
Thus, `-o foo` and `-ofoo` are equivalent.

But mainly, option parsing stops when the first `argv[]` element is
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
option parsing will do, but I found a balance that feels right to
me. To specify and parse the options of the hypothetical `blark`
program used as example above, all we need is this:

    import pgetopt

    ovc, args = pgetopt.parse({
        "v": ("verbose", bool, False, "be verbose"),
        "o": ("output_file", str, "/dev/stdout", "output file", "PATHNAME"),
        "i": ("iterations", int, 1, "number of iterations"),
        "_arguments": ("gnumm", "..."),
    })

The `parse()` function has, in the usual case, one argument, a
dictionary describing the options. The single-letter string key is
the option letter; its value is the option descriptor, an iterables
(usually a tuple or a list) of four or five elements. These are:

1. the name of the option in the namespace returned, also (with `_`
   replaced by `-`) the name of the corresponding long option
2. the type: `bool` (boolean, actually a counter), `str` (needs
   argument), `int` (needs integer argument)
3. the default value (or counter start in case of bool); it may be
   a list collecting the arguments of multiple occurrances of the
   option
4. the text for the help output
5. [optional] a placeholder for the argument for help output

IMO these descriptors with 4 or at most 5 elements are short enough
to use positional parameters without sacrificing clarity or ease of
use. So, as there are no named parameters, there is little clutter,
keeping the whole thing short and easy to read.


Then, there may be a few key/value pairs where the key is one of
these keywords:

`_arguments` : either a string describing the command's arguments,
or an iterable with those. In the latter case, it is used to
determine the minimum and maximum number of arguments. See below at
"Argument count checking" for more information.

`_help_header`
: a string that will be printed at the top of the help message.

`_help_footer`
: a string that will be printed at the bottom of the help message.

The two values returned are an option value container — a namespace
in which the values can be accessed using the option name (e.g. as
`ovc.verbose`, `ovc.output_file`) — and a list with the remaining
arguments.

And that is indeed all you need to know for the majority of
applications. One simple example exercises nearly all features of
this package:

    import pgetopt

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

After this call, the option value container `ovc` contains (among
others) the following attributes:

| Attribute         | Value                                                 |
|-------------------|-------------------------------------------------------|
| `ovc.schmooze`    | the number of `-s` options counted                    |
| `ovc.output_file` | the parameter of `-o` or `--output-file`, or `None`   |
| `ovc.repetitions` | the parameter of `-n` or `--repetitions`, or `3`      |
| `ovc.debug`       | a list with all parameters given to `-d` or `--debug` |

(See the `schmooze.py` program in the `examples/` directory to see
this in the context of a program.)

When the program is called with an invalid option or the wrong
number of arguments (in this case: none), or when it sees the `-?`
or `--usage` option, a corresponding error and a brief usage message
are printed and the program exits with an exit status of 64. When
the program is called with `-h` or `--help`, a more detailed help
message is printed, consisting of the usage, the `_help_header`
value (if present), an explanation of the options constructed from
the option descriptors, and the `_help_footer` value (if present).

The help and usage messages are available from the option value
container by calling the `ovc_help_msg` and `ovc_usage_msg` methods,
which return the respective message. Or call the `ovc_help` and
`ovc_usage` methods, which print their message and end the program.

You can override the `-?`/`--usage` and the `-h`/`--help` options by
specifying your own descriptor for these options in the descriptors
dictionary. However, you cannot override the `--usage` option with
any other short option than `-?`, or `--help` with any other short
option than `-h`, as the short options are the decisive parameters
here.


Argument count checking
-----------------------

As mentioned above, if the `_arguments` field of the options
descriptor is an iterable, the number of actual arguments is checked
against the minimum and maximum number of arguments derived from
this sequence. This is intended to capture the tradition of Unix
command argument synopses and works as follows:

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
and given that this is rarely needed, I chose to omit that. It can
be done in the application just as well.


The `parse()` function
----------------------

Above, the `parse()` function has been shown to be called with one
argument only, the option descriptors dictionary. There are two
optional arguments that can be useful in some applications:

`args`: The actual argument list from which the options shall be
parsed. By default, this is taken from `sys.argv[1:]`, which will be
adequate in most cases. But if, for instance, a program has
subcommands that in turn have their own options and arguments, the
subcommand's argument list can be passed here explicitly.

`exit_on_error`: If this value is true, which it is by default, the
`ovc_usage()` method will be called to print an error message and
exit the program when an invalid option, a missing option argument,
or the wrong number of arguments is seen. If it is false, an
exception is raised instead. These exceptions are listed below.


Exceptions
----------

When an invalid option, a missing option argument, or the wrong
number of arguments is seen in the argument list, an exception is
raised. Every one of these exceptions has two arguments, a message
and an object (the option in question or the minimum or maximum
number of arguments). These are as follows:

| Type       | Message                             | Argument |
|------------|-------------------------------------|----------|
| IndexError | "too few arguments, needs at least" | minimum  |
| IndexError | "too many arguments, at most"       | maximum  |
| KeyError   | "unknown option"                    | option   |
| TypeError  | "option does not take an argument"  | option   |
| IndexError | "option needs argument"             | option   |
| TypeError  | "value for option must be integer"  | option   |

(The option argument is the option as found on the command line,
meaning it can be the short form or the long form.)

If you want to handle these exception by yourself, see the `parse()`
function for an example.

In addition to these exceptions, an `AssertionError` exception can
be thrown in the following cases:

 * An option descriptor is not an iterable of length 4 or 5.
 * The name of an option in the descriptor is not a string.
 * The specified type of the option is not `bool`, `int`, `str`, or
   `None`.


The OptionValueContainer
------------------------

The `OptionValueContainer`, short OVC and in my code often `ovc`, is
the first of the two values returned by the `pgetopt.parse()`
function. When it is returned, it contains the option values as
attributes with the names of the options. So, if an option has been
specified as `"v": ("verbose", bool, False, "turn on verbose mode")`
in the option descriptors argument, its value is available as
`ovc.verbose` in the returned OVC.

Besides that, there are a few other fields in the OVC that may be of
interest. Their names begin with `ovc_` or `_` to avoid conflicts
with option names.

`ovc.ovc_usage`: Method that prints a brief usage message describing
the command arguments (from the `_arguments` value) and a reference
to the `-h` option, and then exits the program. This is used
internally when the actual options or the number of arguments are
incorrect, but it can also be used by the user. Optional argument
`error` may contain an error message that is printed with the usage
message; optional argument `exit_status` may specify the exit status
used (default: 2)

`ovc.ovc_usage_msg`: Method that returns the usage message mentioned
above as a string.

`ovc.ovc_help`: Method that prints a more detailed help message and
exits the program. The help message consists of the usage message
(see above), the `_help_header` argument of the descriptors
dictionary to `parse()`, a description of the options (constructed
from the descriptors), and the `_help_footer` argument.

`ovc.ovc_help_msg`: Method that returns the above help message as a
string.

The other fields, whose names begin with `_`, are not meant as
official interfaces, but could be subject to change in future
versions.

`ovc._args`: The arguments as passed to the `parse()` function or,
by default, taken from `sys.argv[]`.

`ovc._arguments`, `ovc._help_footer`, `ovc._help_header`: The
corresponding fields of the descriptors argument.

`ovc._have_opt`: Method used internally during option parsing.

`ovc._long`: Option descriptors dictionary by long option name.

`ovc._max`: Maximum number of arguments as calculated from the
`_arguments` description, or None.

`ovc._opts`: Option descriptors dictionary by short option name.

`ovc._min`: Minimum number of arguments as calculated from the
`_arguments` description, or None.

`ovc._parse`: Method used internally for option parsing.

`ovc._program`: The name of the program, from `sys.argv[0]`.

`ovc._set_optarg`: Method used internally during option parsing.


Limitations
-----------

The simple interface and the brevity of the implementation result in
a few limitations.

 * There can be no single-letter option without a corresponding long
   option and vice versa.

 * Checking for errors in the passed option descriptors dictionary
   is rudimentary (see "Exceptions" above).

 * Passing an argument to the help option in the same `argv[]`
   element (as in `--help=3`) results in `ovc.help` being set to
   that value, and not in a call to the `ovc_help` method.


Semi-hidden feature: option value callbacks
-------------------------------------------

A feature not mentioned so far is the ability to call a function
when an option is encountered. If the type of an option is specified
as `None` and the default value is a callable function, this
function will be called when the option is encountered on the
command line, and its return value (which must not be `None`) will
be used as the option's value.

This is not a fully planned feature; rather, it fell more or less
accidentally out of the implementation of the default `help` and
`usage` options. At the moment I do not really see a useful
application, but maybe someone else will.

I have to admit this feature isn't the prime example for clarity of
the user interface. But then it was an afterthought and can safely
be just ignored.


Documentation, Examples and Testing
-----------------------------------

This README file is the main documentation. The source is in the
`lib/` directory; run `make` in the main directory to update the
`README.md` with a table of contents. The package README in
`package/` contains the "schmooze" example. The docstring of the
`parse()` function contains a concise summary of the main features
and usage of the module.

The examples shown above can also be found in the `examples/`
directory.

The directory `tests/` contains a test suite, which is still
somewhat work in progress. It can be invoked by running `make test`
in the main directory.


Building the PyPi package
-------------------------

The PyPi package is built and uploaded to PyPi by running `make pkg`
and `make upload`, respectively. The package URL is
<https://pypi.org/project/pgetopt-jyrgenn/>.


[Juergen Nickelsen <ni@w21.org> 2020-05]
