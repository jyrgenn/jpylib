
jpylib Package
==============

The `jpylib` package is meant to be a library of things I want to
have at hand for my own daily python programming. It shall include
all the things I have developed and want to re-use — modules, small
utility functions, and things. These are more or less independent
functionalisties that I didn't find readily available in the usual
libraries in the way I like them. Some are present, like
command-line option argument parsing, but not in a way that I find
convenient to use; others are not found at all.

This documentation is a work in progress.


The Package
-----------

`jpylib` is a PyPi package (as `jpylib-jyrgenn`) so I can access it
from everywhere, install it using pip, and import it into programs
as a whole. That could look like this:

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

See https://pypi.org/project/jpylib-jyrgenn


`alerts` – print messages depending on an alert level
-----------------------------------------------------


`config` — reading configuration values from files
--------------------------------------------------

Supports config files as Python code and strings in a simple
`key=value` syntax.


`fntrace` — function call tracing decorator
-------------------------------------------

    # trace calls of this function
    @y.tracefn
    def foo(bar, moo=None):
        pass

Uses the `trace` function of the `alerts` module, so the alert level
must be L_TRACE or higher to have the output printed.


`kvs` — simple key-value string parser
--------------------------------------

Parser for key-value strings like
"foo=bar,dang=[1,2,15],d={a=b,c=[d,e,f]}".

The data is returned as a Python data structure composed of strings,
dictionaries, and lists. It is used to set configuration values from
command-line arguments with a syntax more compact than e.g. JSON.

Syntax:

 * On the top level, the key-value string is a kvpairs list.

 * A kvpairs list is a list of zero or more key=value pairs
   separated by commas. It is mapped to a Python dictionary.
   Example: "signals=[1,2,15],action=terminate"

 * A key is a string that does not contain curly brackes, brackets,
   a comma, or an equals sign. Leading whitespace is not considered
   part of the key; trailing or embedded whitespace is a syntax
   error. For configuration values, it is helpful to match the
   syntax of Python identifiers, i.e. first character an underscore
   or a letter, following characters, if any, underscore, letter, or
   digit. These are mapped to Python dictionary keys. Example:
   "key_file"

 * A value can be a literal, a dictionary, or a list of values.

 * A literal value is a string of characters that doesn't contain
   curly brackes, brackets, a comma, or an equals sign. Whitespace
   is considered part of the literal. These are mapped to Python
   strings. Example: "Radio Dos"

 * A dictionary is a kvpairs list enclosed by curly braces. Example:
   "{file=~/etc/foo.conf,syntax=INI}"

 * A list is a list of zero or more values separated by commas and
   enclosed in brackets. Example: "[HUP,INTR,TERM]"

This syntax is obviously limited, but sufficient to express complex
data structures with (some) string values as leaves. It is mainly
meant to be compact for use on the command line.

The parser is somewhat sloppy and will accept some deviations from
this descriptsion, but exploiting this sloppyness will not be of any
use.

    parse_kvs(string, intvals=False):
       """Parse a key=value string and return the data structure."""


`namespace` — a namespace value container class
-----------------------------------------------

    class Namespace:
        """Simple name space class as a key-value store.

        Values can be assigned and read directly (ns.key = value) or
        using the set()/get() methods. An update() method (as with a
        dictionary) has the options to skip keys beginning with an
        underscore, or raise a KeyError if a key is not previously
        known.

        """

        __init__(self, **kwargs):
            Initialize a Namespace object from the 'kwargs' mapping.

        update(self, new_values, skip_underscore=False, reject_unknown=False):
            Update the object with a dictionary of new key/value
            pairs.

            If `reject_unknown` is true, it is an error if the
            argument dictionary contains keys that are not in the
            object's key set.

            If `skip_underscore` is true, keys that start with an
            underscore ("_") are not considered for update.

        set(self, key, value):
            Set a value.

        get(self, key, default=None):
            Get a value; default if key is not present.

Also `__str__` and `__repr__`.


`pgetopt` — a submodule `pgetopt` as used elsewhere
---------------------------------------------------

Usage pattern:

    ovc, args = y.pgetopts({
        # letter: (name, type, default, description [, arg_doc])
        "v": ("verbose", bool, False, "be verbose"),
        "o": ("output_file", str, "/dev/stdout", "output file", "PATHNAME"),
        "i": ("iterations", int, 1, "number of iterations"),
        # _arguments: [...] | _help_header: "..." | _help_footer: "..."
        "_arguments": ["gnumm", "..."],
    })

    y.pgetopts(descriptors, args=sys.argv[1:], exit_on_error=True),
    ovc.ovc_help(), ovc.ovc_help_msg(), ovc.ovc_usge_msg(),
    ovc.ovc_usage(error="", exit_status=64), ovc.ovc_values()

Also, `y.verbosity_option` can be used as the option description for
the `-v` option – variable name "verbose", default value is
L_NOTICE, each occurence of `-v` increases the alert level.


See the `pgetopt` documentation for details.


`getsecret` — read a secret from a secrets file
-----------------------------------------------

    putsecret(key, value, fname=None, options=None,
                  char_encoding=default_char_encoding):
        Put a secret tagged with `key` into the secrets file `fname`.

        A backup copy is made as {fname}.backup. A temporary file
        named .../.{basename}.newtmp is created, which also serves
        as a lockfile. After all records are written to the
        temporary file, it is moved into place, deleting the
        original secrets file.

    getsecret(key, fname=None, char_encoding=None, error_exception=True):
        Get a secret tagged with `key` from the secrets file `fname`.

        The default pathname for the secrets file is `/etc/secrets`
        if called by root, and `$HOME/etc/secrets` for normal users.

        The file consist of lines of the form `_key_:_value_`, so
        the key may not contain a colon. Whitespace is significant
        except at the end of the line, where it will be stripped, so
        the secret may not end with whitespace. You can get around
        these limitations by encoding key and/or value with e.g.
        base64.

        If the key is found, the value is returned. Otherwise, a
        `KeyError` exception is raised. The exception's arguments
        are a format string, the key, and the file name. (Splitting
        this up allows for subsequent i18n.)

        If the found value for the key starts with "{b64}", it will
        be base64-decoded before it is returned.

Also, command-line tools of the same respective name.


`sanesighandler` — handle SIGINT and SIGPIPE
--------------------------------------------

Decorator: exit the program silently on SIGINT and SIGPIPE like
Dennis and Ken intended.

Usage pattern:

    @y.sanesighandler
    def main():
        # do something
        ...

    if __name__ == "__main__":
        main()



`program`, `home`, `real_home`, `version` – variables
-----------------------------------------------------

A few variables:

`y.program`: the basename of `sys.argv[0]`, convenient to use in
usage and error messages.

`y.home`: The home directory of the user. This is $HOME from the
environment, if present, otherwise `y.real_home` (which can always
be determined).

`y.real_home`: the home directory entry of the uid of the running
process. This may be different from $HOME when running `sudo -s`.

`y.version`: the version number of the `jpylib` package.


`outputCaptured`, `outputAndExitCaptured` – context managers
------------------------------------------------------------

    outputCaptured():
        Context manager to capure output to stdout and stderr.

        This works by temporarily replacing sys.stdout and sys.stderr with
        StringIO ports; these are both returned, so the output of the code
        run on the context can be retrieved from them:

            with outputCaptured() as (out, err):
                ...
            theOutput = out.getvalue()        # stdout output as string
            theErrout = err.getvalue()        # stderr outout as string

    outputAndExitCaptured():
        Context manager to capture output to stdout/stderr and exit status.

        Like with outputCaptured(), stdout and stderr are captured in the
        returned StringIO objects. In addition, the exit status in case of a
        sys.exit() is captured in the `value` property of the returned
        status object:

            with outputAndExitCaptured() as (out, err, status):
                ...
            theOutput = out.getvalue()    # stdout output as string
            theErrout = err.getvalue()    # stderr outout as string
            theStatus = status.value      # sys.exit() argument (or 0 or None)

        The status value is None if the code run in the context hasn't
        called sys.exit().



`backquote` — get output of an external command
-----------------------------------------------

    backquote(command, shell=None, full_result=False, silent=False):
        Similar to Perl's `command` feature: run process, return result.

        If command is a tuple or a list, run it directly. Otherwise, make it a
        string if necessary and:

            If shell is True, run command as shell command line with
            "/bin/sh".

            If shell is otherwise true, use it as the shell and run
            command in it.

            If shell is None (or unspecified), run command with
            "/bin/sh" if it contains shell meta characters.
            Otherwise, split the string into a list and run it
            directly.

            If shell is otherwise false, split the string into a
            list and run it directly.

        If full_result is false (the default), return only stdout as
        a string. In this case, a ChildProcessError is raised if the
        exit status of the command is non-zero or stderr is not
        empty. This can be suppressed by setting silent to true.

        If full_result is true, return a tuple of (stdout, stderr,
        exit status). No exception for exit status or stderr is
        raised, regardless of the value of silent.

        In any case, however, there will be an exception raised if the
        called program cannot be found.


`boolish` — make bool values from strings
-----------------------------------------

    def boolish(value, default=None)
        Return a truth value for the argument.

        If that cannot be determined, fall back to default (if not
        None) or raise a ValueError exception. This can be used for
        parsing config files (that aren't Python) or interactive
        answers or the like.

recognised strings for True: yes y sure ja j jou si on oui t true
aye 1 affirmative

recognised strings for False: no n nope nein nee off non f false nay
0 negative

`y.means_true` and `y.means_false` are sets of strings that can be
adapted to application needs.


`flatten` — generator, flatten a sequence (except strings
---------------------------------------------------------


`maybe_int`, `maybe_num` — return number represented by a string
----------------------------------------------------------------

    maybe_int(arg):
        Return the corresponding int if the arguments represents one, or None.

    maybe_num(arg):
        Return the corresponding int or float if arg represents one, or None.


`is_int`, `is_num` — check if the argument is a number
------------------------------------------------------

    is_int(arg):
        Return True if the arguments represents an int, or False.

        The argument may be not an int (maybe e.g. a string), but if it
        can be read as an int, it represents an int.

    is_num(arg):
        Return True if the arguments represents a number, or False.

        The argument may be not numeric (maybe e.g. a string), but if it
        can be read as a number, it represents a number.


`flatten` — flatten nested sequence
-----------------------------------

    flatten(seq):
        Flatten a nested sequence into a flat one with the same elements.

        Return a flat generator object containing just the elements. If the
        argument is a string or not a sequence, the generator object will
        contain just the argument.


`is_sequence` — check if argument is a sequence
-----------------------------------------------

    is_sequence(arg):
        Return True iff the argument is a sequence other than string.


`Table` — an ASCII table formatter, with optional templates
-----------------------------------------------------------

    format_table(data=None, template_name=None, template=None, **kwargs):
        Format a table from the specified data and (optional) template.

        The template can be given by name, selecting one of the
        pre-defined templates, or explicitly. In absence of a
        specified template, the default parameters will be used,
        which is equivalent to the "minimal" template.

        All parameters can be tweaked through the kwargs, which are
        passed to the Table constructor (see there).


