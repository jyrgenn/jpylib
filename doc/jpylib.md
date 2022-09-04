
jpylib Package
==============

The `jpylib` package is meant to be a library of things I want to
have at hand for my own daily python programming. It shall include
all the things I have developed and want to re-use — modules, small
utility functions, and things. These are more or less independent
functionalities that I didn't find readily available in the usual
libraries in the way I like them. Some are present, like
command-line option argument parsing, but not in a way that I find
convenient to use; others are not found at all.

(If any of this is indeed in the standard library and I just missed
it, I'll appreciate a hint.)

This documentation is a work in progress.


[[_TOC_]]


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

Print alerts and other messages depending on an alert level. Current
levels:

|Level     | value |
|----------|------:|
|`L_ERROR`   | 0     |
|`L_NOTICE`  | 1     |
|`L_INFO`    | 2     |
|`L_DEBUG`   | 3     |
|`L_TRACE`   | 4     |

Defaults:

    Config(
            # decoration to print before a message, per level
            decoration=["{cfg.program}: Error:", None, None, "DBG", "TRC"]

            # program name to use in a message
            program=os.path.basename(sys.argv[0]),
            
            # syslog facility; if set, syslog will be used
            syslog_facility=None,

            # syslog priority, per level
            syslog_prio = [
                syslog.LOG_ERR,
                syslog.LOG_NOTICE,
                syslog.LOG_INFO,
                syslog.LOG_DEBUG,
                None,                   # don't let this go to syslog
            ],
            
            # status: syslog has been opened
            syslog_opened=False,
            
            # fd to print message to, per level
            fd=[2, 2, 2, 2, 2]

            # current alert level
            level=L_NOTICE,
            
            # maximum alert level
            max_level=len(alert_levels)-1,

            # print timestamps with messages (false, or a function)
            timestamps=False,

            # had any errors yet?
            had_errors=False,
        )

Functions:

    alert_config(*, decoration=None, fd=None, level=None, program=None,
                 syslog_facility=None, syslog_prio=None, reset_defaults=None,
                 timestamps=None):
        Reset everything to the specified or default values.

    alert_redirect(level, file):
        Redirect printing of alerts from `level` to `file`.

    alert_level(level=None):
        Get or set the verbosity level for the alert functions.

        err() will print something with level 0 (and greater), i.e. always.
        notice() will print something with level 1 (and greater).
        info() will print something with level 2 (and greater).
        debug() will print something with level 3 (and greater).
        trace() will print something with level 4 (and greater).

        This function can be used to set the default alert level in
        a pgetopts() option descriptor, e.g. for the "-v" option.

    alert_level_name(level=None):
        Return the name of the specified (or current) level number.

    alert_level_up():
        Increase the alert level by one.

        This is intended to be used as the callback function for the
        value of a pgetopts option to increase the verbosity.

    alert_level_zero():
        Set the alert level to zero (errors only).

        This is intended to be used as the callback function for the
        value of a pgetopts option to set the verbosity to zero.

    is_notice():
        Return True iff the alert level is at least at notice.

    is_info():
        Return True iff the alert level is at least at info.

    is_debug():
        Return True iff the alert level is at least at debugging.

    is_trace():
        Return True iff the alert level is at least at tracing.

    temporary_alert_level(level):
        Context manager to temporarily change the alert level.

    debug_vars(*vars):
        Print debug output for the named variables if is_debug().

The following functions print a message according to the alerts
setup if the respective alert level is given. With the simple
functions, the arguments are joined with blanks; the *f() variants
take a format string and the values to be formatted as arguments.

    err(*msgs), errf(template, *args):
        Print error level output.

    fatal(*msgs, exit_status=1), fatalf(template, *args, exit_status=1):
        Print error level output and terminate the program.

    notice(*msgs), noticef(template, *args):
        Print notice level output according to alert level.

    info(*msgs), infof(template, *args):
        Print info level output according to alert level.

    debug(*msgs), debugf(template, *args):
        Print debug level output according to alert level.

    trace(*msgs), tracef(template, *args):
        Print debug level output according to alert level.


Together with the `pgetopts()` function for option parsing ([see
there for
details](./pgetopts.md#semi-hidden-feature-option-value-callbacks)),
a useful pattern of alerts usage in the options specification of a
simple CLI program goes like this:

    ovc, args = y.pgetopts({
        "q": ("quiet", y.alert_level_zero, y.alert_level(y.L_NOTICE),
              "be quiet (no output except error messages)"),
        "v": ("verbose", y.alert_level_up, y.alert_level(y.L_NOTICE),
              "increase verbosity (up to 3 make sense)"),
        ...
    })

Here, `y.alert_level(y.L_NOTICE)` sets the initial alert level
value. (It does that twice, but this redundancy can be tolerated to
benefit the clarity of expression.) Using the functions
`alert_level_zero` and `alert_level_up` instead of an option type
makes these functions called when their respective option is seen on
the command line. This sets the alert level directly, with no
further action from the program needed.

Please note that in this usage, the option value container fields
`ovc.quiet` and `ovc.verbose` no longer reflect the actual alert
level setting. But because the occurences of the options alone set
the alert level through the function calls `alert_level_zero()` and
`alert_level_up()` already, this is no longer necessary.


`config` — reading configuration values from files
--------------------------------------------------

Supports config files as Python code and strings in a simple
`key=value` syntax. The Config object is a namespace, so values can
be retrieved using both `cfg.get("key")` or, often more convenient
and clear, `cfg.key`.

The Config object is initialised with `**kwargs`, denoting the
config variables and their values. A loaded config file is run as
Python code (and so must not contain untrusted contents), and all
variables defined in its global level are seen as updates to the
config variables as long as their names do not begin with an
underscore (`_`). By default, all keys that are not already
contained in the initialised Config object are seen as errors
(unless `reject_unknown` is false).

Usage pattern:

    cfg = y.Config(                           # define default configuration
        threads_max = 10,                     # maximum number of threads
        default_interval = 60,                # check run interval in seconds
        external_from = "external_checks",    # in the config dir
    )

    cfg.load_from(config_path)
    cfg.update_from_string("threads_max=20")

Config class:

    class Config(Namespace):
        Name space class used to build a config object.

        def update(self, new_values, reject_unknown=True):
            Update the Config with new values.

            If reject_unknown is True (which is the default), keys
            that do not yet exist will be rejected.

        def set(self, key, value, reject_unknown=True):
            Set a config value for a key.

            If reject_unknown is True (which is the default), keys
            that do not yet exist will be rejected.

        def get(self, key):
            Get a value from the config.

        def load_from(self, filename, reject_unknown=True,
                      file_must_exist=True):
            Load a configuration from file 'filename'.

            If reject_unknown is True (which is the default), keys
            that do not yet exist will be rejected.

        def load_config_files(self, config_files, notice_func=None,
                              reject_unknown=True, files_must_exist=False):
            Read the configuration from the config files.

            If reject_unknown is True (which is the default), keys
            that do not yet exist will be rejected.

            Optional "notice_func" is a function to print a message
            about a config file being loaded.

        def update_from_string(self, cfgstring,
                               reject_unknown=True, intvals=True):
            Update the configuration from a key-value string.

            This can be used to pass config snippets on the command
            line. The string can look like e.g. this:

            "foo=bar,dang=[1,2,15],d={a=b,c=[d,e,f],quux=blech},e=not"

            If reject_unknown is True (which is the default), keys
            that do not yet exist will be rejected.


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


`pgetopts` — PODIX-compliant command-line options parsing
---------------------------------------------------------

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
`L_NOTICE`, each occurence of `-v` increases the alert level.


See the [`pgetopts`](./pgetopts.md) documentation for details.


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


`input_from`, `outputCaptured`, `outputAndExitCaptured` – context managers
--------------------------------------------------------------------------

    inputFrom(input)
        Context manager to redirect stdin from an open file.

        This works by temporarily replacing sys.stdin with an open file.
        Typical code would look like this:

            with open(inputFile) as input:
                with inputFrom(input):
                    ...                       # code with input as sys.stdin


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


`maybe_int`, `maybe_num` — return number represented by a string
----------------------------------------------------------------

    maybe_int(arg):
        Return the corresponding int if the arguments represents one, or None.

    maybe_num(arg):
        Return the corresponding int or float if arg represents one, or None.


`remove_outliers`, `avc_midrange` — statistics functions
--------------------------------------------------------

    remove_outliers(values):
        Return a copy of the values with the highest and lowest value removed.

        If there is more than one highest or lowest value, only one of them is
        removed.

    avg_midrange(values):
        Return the arithmetic mean of the highest and lowest value of values.


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


`identity` — return just the argument
-------------------------------------

    identity(arg):
        Return `arg`.

This can be helpful to avoid special-casing where a transformation
function can be used, but in some cases none is required.


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


`all_input_lines` — re-implement Perl's diamond operator (<>)
-------------------------------------------------------------

    all_input_lines(fnames=[], cont_err=False):
        Like Perl's diamond operator <>, return lines from files or stdin.

        (Generator) If fnames is empty, return lines from stdin, otherwise
        lines from the named files, in succession. The file name "-" stands
        for stdin. Typically, something like sys.argv[1:] would be passed
        as an argument. If cont_err is true, continue after an error,
        printing an error message. If cont_err is a callable, call it with
        the file name and the exception on error.


`read_items` — read lines/items from a file
-------------------------------------------

    read_items(fname, lstrip=True, rstrip=True, comments_re="^\\s*#",
               skip_empty=True, skip_comments=True, cont_err=False):
        Read lines/items from one or more files (generator).

        With the defaults, comment (`# ...`) and empty lines are skipped, and
        whitespace is stripped from the left and right ends of each line.

        `fname` is the name of the file to read; `-` may be used for stdin.

        If `lstrip` is True, whitespace will be stripped from the left side of
        each line. If it is a string, it specifies the characters to be stripped.

        If `rstrip` is True, whitespace will be stripped from the right side of
        each line. If it is a string, it specifies the characters to be stripped.

        If `strip_newline` is true, newlines will be stripped from the line even
        if `rstrip` does not contain the newline character.

        `comments_re` is used to match comment lines to be skipped (after the
        stripping of whitespace or other characterns is done).

        If `skip_comments` is false, comments will be skipped without regard
        for `comments_re`.

        If `skip_empty` is true, lines that are empty after the stripping of
        whitespace (or what else is specified) are skipped.


`read_mapping` – read a key/value mapping from a file
-----------------------------------------------------

    read_mapping(fname, sep=None, skip_fails=False):
        Read a key/value mapping from `fname`.

        The input are lines of the form "key value", with key and value
        separated by `sep` or whitespace. Comment and empty lines are skipped
        as per the default behaviour of `read_items()`.


`Multiset` — a multiset implementation
--------------------------------------

A multiset is similar to a set, only it can keep multiples of one
thing.

    class Multiset:
        """A multiset implementation."""

    __init__(self, things=()):
        Initialise a Multiset with, optionally, a bunch of things.

    add(self, thing):
        Add a thing to the Multiset.

    count(self, thing):
        Get the number of a specific thing in the Multiset.

    set_count(self, thing, count):
        Set the number of a specific thing in the Multiset.

    remove(self, thing, completely=False):
        Remove one of or all of a specific thing from the Multiset.

    items(self):
        Return all items in the Multiset. Also, iteration helper.

    __iter__(self):
        Iterate over the items in the Multiset, for `for t in ...`.

    __str__(self):
        Return a string representation of the Multiset (parsable).

    __repr__(self):
        Return a string representation of the Multiset (parsable).

