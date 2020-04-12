#!/usr/bin/env python3
# -*- fill-column: 72 -*-

"""POSIX-compatible command-line option parser with long options.
See the documentation of the parse() function for more information.
"""

import os
import sys
import copy
from collections.abc import Iterable

debug = True


class OptionValueContainer:
    def __init__(self, descriptors):
        """The argument is a dict with optchar as key, descriptor as value.

        The option descriptor is a tuple with the name, type, default
        value, and help text; optionally an argument name. The type is
        bool (argument-less, also counts) or int (with int argument) or
        str (with str argument) or a callable. See the documentation of
        the parse() function below for more information.

        """
        self._program = os.path.basename(sys.argv[0])
        self._opts = descriptors
        for opt, desc in descriptors.items():
            if opt.startswith("_"):
                continue                # allow for _<keyword> entries
            assert isinstance(desc, Iterable) and len(desc) in (4, 5),\
                f"descriptor of option '{opt}' not iterable len 4 or 5"
            assert isinstance(desc[0], str),\
                f"name of option '{opt}' not a string"
            assert desc[1] in (bool, int, str) or callable(desc[1]),\
                f"invalid type option '{opt}': {desc[1]}"
            self.__dict__[desc[0]] = desc[2]

        if "h" not in self._opts:
            self._opts["h"] = ("help", self._help, None, "show help on options")
        if "?" not in self._opts:
            self._opts["?"] = ("usage", self._usage, None, "show usage briefly")
        for field in "_arguments", "_help_header", "_help_footer":
            self.__dict__[field] = self._opts.get(field)
        self._long = { desc[0] : desc for desc in self._opts.values() }


    def __str__(self):
        """Return a string representation of the OptionValueContainer."""
        sep = "\n    " if debug else ""
        return self.__class__.__name__ + "<" + sep + (", " + sep).join(
            [f"{k}={repr(self.__dict__[k])}" for k in sorted(self.__dict__)])\
            + sep + ">"


    def _parse(self, args):
        self._args = args
        while self._args and self._args[0].startswith("-"):
            arg = self._args.pop(0)
            if arg == "--":
                break
            if arg.startswith("--"):
                self._have_option(arg[2:].replace("-", "_"), True)
            else:
                for c in arg[1:]:
                    self._have_option(c, False)
        self._check_argc()
        return self, self._args


    def _check_argc(self):
        """Check the argument count if _arguments is a list or tuple."""
        if isinstance(self._arguments, (list, tuple)):
            min = max = 0
            ellipsis = False
            for arg in self._arguments:
                if arg.startswith("["):
                    # for optional arguments like "[op1 op2 op3]"
                    max += len(arg.split(" "))
                if arg.count("..."):
                    ellipsis = True     # eliminate max; don't increase min
                else:
                    min += 1
                    max += 1
                # BUG: min increased if [
            if not ellipsis and len(self._args) > max:
                raise IndexError(f"too many arguments, at most", max)
            if len(self._args) < min:
                raise IndexError(f"too few arguments, needs at least", min)
        

    def _have_option(self, opt, is_long_option):
        value = None
        if is_long_option:
            parts = opt.split("=", 1)
            if len(parts) > 1:
                opt, value = parts
            if opt not in self._long:
                raise KeyError(f"{self._program}: unknown option", f"'--{opt}'")
            desc = self._long[opt]
        else:
            if opt not in self._opts:
                raise KeyError(f"{self._program}: unknown option", f"'-{opt}'")
            desc = self._opts[opt]
        name, typ, *_ = desc
        if typ == bool:
            self.__dict__[name] += 1
        elif typ in (str, int):
            self._set_optarg(opt, desc, value)
        elif callable(typ):
            self._set_optarg(opt, desc, typ())


    def _set_optarg(self, opt, desc, value):
        if value is None:
            value = self._args.pop(0)
            print("value is", value)
        name = desc[0]
        if desc[1] == int:
            print("should be int", value)
            try:
                value = int(value)
            except:
                raise TypeError(f"value for '{name}' option must be integer:",
                                repr(value))
        if isinstance(self.__dict__[name], list):
            self.__dict__[name].append(value)
        else:
            self.__dict__[name] = value


    def _values(self):
        """Return the option values as a dictionary."""
        return {
            opt: self.__dict__[opt]
            for opt in map(lambda desc: desc[0], self._opts.values())
            if opt in self.__dict__
        }


    def _help(self, exit_status=0):
        print(self._help_message(),
              file=sys.stdout if not exit_status else sys.stderr)
        sys.exit(exit_status)

        
    def _help_message(self):
        msg = self._usage_message() + "\n"
        if self._help_header:
            msg += self._help_header + "\n\n"
        for opt in sorted(self._opts.keys()):
            if opt.startswith("_"):
                continue
            desc = self._opts[opt]
            arg = ""
            if desc[1] in (str, int):
                arg = (desc[4] if len(desc) == 5 else "ARG")
            msg += \
                f" -{opt}, --{desc[0].replace('_', '-')} {arg}\n    {desc[3]}"
            if desc[1] in (int, str):
                msg += f" ({desc[1].__name__} arg, default: {repr(desc[2])})"
            msg += "\n"
        if self._help_footer:
            msg += "\n" + self._help_footer
        return msg


    def _usage(self, error="", exit_status=2, dash_h=True):
        out = sys.stdout if not exit_status else sys.stderr
        if error:
            print(self._program + ":", error, file=out, end="\n\n")
        print(self._usage_message(), file=out)
        if dash_h:
            print("run with '-h' to get help on command options")
        sys.exit(exit_status)


    def _usage_message(self):
        return f"usage: {self._program} [options] {' '.join(self._arguments)}"


def parse(descriptors, args=sys.argv[1:], exit_on_error=True):
    """Parse the command line options according to the specified descriptors.

    Keys of the descriptors dictionary are options or keywords. In case
    of an option, the key is the single option character, and the value
    is an iterable of four or five fields:

      (1) name of the option, used in the returned namespace and as the
      name of the corresponding long option name (after replacing
      underscores with dashes);

      (2) the type of the option, which may be bool for options without
      arguments, or str or int for options with an argument of the
      respective type, or a callable paremeterless function that will be
      called immediately when the option is seen, to return the option
      value;

      (3) the default value, which can be a starting counter (or False)
      for bool options, or an integer or string value for int or str
      options, respectivey, or a list, to which option arguments will be
      appended (for potential multi-value options);

      (4) the description of the option, to appear in the help text;

      (5) the (optional) name of the option's argument for the help
      text (which defaults to 'ARG').

    If the key begins with an underscore, it may be a keyword.
    Recognised keywords are:

      "_help_header": value is a string to be printed with 'help',
      between the usage and the explanation of the options;

      "_help_footer": value is a string to be printed with 'help', after
      the explanation of the options;

      "_arguments": an iterable with the argument names; it is used to
      print the arguments in the 'usage' as well as to determine the
      minimum and maximum number of arguments:
    
         - a normal string counts as one argument towards minimum and
           maximum

         - if it contains '...', the number of arguments is not limited,
           so there is no maximum

         - if it begins with '[', it counts as optional; if it can be
           split by blanks into more than one word, each one counts
           toward the maximum; e.g. "[param1 param2 param3]" increases
           the maximum by 3

    If no '?' or 'h' option is specified, it will default to a 'help' or
    a 'usage' function, respectively, which will be called immediately
    when the option is seen. 'help' prints a description of the option,
    framed by the _help_header and the _help_footer; 'usage' prints a
    brief summary of the program's parameters. Both terminate the
    program after printing their message. (This behaviour can be
    deactivated by setting a '-h' and/or a '-?' option.)

    In case of a normal termination of the parse() function (i.e.
    options and number of arguments okay, or exit_on_error passed as
    false), it returns an OptionValueContainer and the remaining command
    line arguments. Example:

      ovc, args = pgetopt.parse({
        "s": ("schmooze", bool, 0, "increase schmooziness"),
        "o": ("output_file", str, None, "output file (or stdout)", "NAME"),
        "n": ("repetitions", int, 3, "number of repetitions"),
        "d": ("debug", str, [], "debug topics", "DEBUG_TOPIC"),
        "_arguments": ("string_to_print", "..."),
        "_help_header": "print a string a number of times",
        "_help_footer": "This is just an example program.",
      }

    On return, ovc has the following fields:
      ovc.verbose: the number of -s options counted,
      ovc.output_file: the parameter of -o or --output-file, or None
      ovc.repetitions: the parameter of -n or --repetitions, or 3
      ovc.debug: a list with parameters given to all -d or --debug

    Parameters to type int or str options follow in the next argument;
    with long options, "--option=parameter" is also possible.

    Other potentially useful fields of ovc:
      ovc._help(),
      ovc._usage(): the help and usage function, respectively
    
      ovc._help_message(),
      ovc._usage_message(): the corresponding messages as stringsq

    """
    ovc = OptionValueContainer(descriptors)
    try:
        return ovc._parse(args)
    except Exception as e:
        if exit_on_error:
            ovc._usage(" ".join(map(str, e.args)), exit_status=1)
        raise(e)


if __name__ == "__main__":
    ovc, args = parse({
        "s": ("schmooze", bool, 0, "increase schmooziness"),
        "o": ("output_file", str, None, "output file (or stdout)", "NAME"),
        "n": ("repetitions", int, 3, "number of repetitions"),
        "d": ("debug", str, [], "debug topics", "DEBUG_TOPIC"),
        "_arguments": ("string_to_print", "..."),
        "_help_header": "print a string a number of times",
        "_help_footer": "This is just an example program.",
    }, exit_on_error=True)
    print(ovc._values(), args)
