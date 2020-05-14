#!/usr/bin/env python3
# -*- fill-column: 72 -*-

"""POSIX-compatible command-line option parser (plus long options).
See the parse() function for more information.
"""

import os
import sys
import copy


class OptionValueContainer:
    def __init__(self, descriptors, args):
        """Arguments: dict optchar => descriptor, and the command-line args.

        The option descriptor is a tuple with the name, type, default
        value, and help text + optional argument name. See the parse()
        function below for more information.

        """
        self._program = os.path.basename(sys.argv[0])
        self._opts = copy.deepcopy(descriptors)
        for opt, desc in self._opts.items():
            if opt.startswith("_"):
                continue                # allow for _<keyword> entries
            assert hasattr(type(desc), '__iter__') and len(desc) in (4, 5),\
                f"descriptor of option '{opt}' not sequence len 4 or 5"
            assert isinstance(desc[0], str),\
                f"name of option '{opt}' not a string"
            assert desc[1] in (bool, int, str),\
                f"invalid option type '{opt}': {desc[1]}"
            self.__dict__[desc[0]] = desc[2]
        if "h" not in self._opts:
            self._opts["h"] = ("help", None, self._help, "show help on options")
        if "?" not in self._opts:
            self._opts["?"] = ("usage", None, self._usage, "show usage briefly")
        for field in "_arguments", "_help_header", "_help_footer":
            self.__dict__[field] = self._opts.get(field)
        self._long = { desc[0].replace("_", "-") : desc
                       for desc in self._opts.values() }
        self._args = args


    def _parse(self):
        while self._args and self._args[0].startswith("-"):
            arg = self._args.pop(0)
            if arg == "--": break
            if arg.startswith("--"):
                self._have_opt(arg[2:])
            else:
                for c in arg[1:]:
                    self._have_opt(c)
        # check number of arguments if specified in _arguments
        if isinstance(self._arguments, (list, tuple)):
            min = max = 0
            inf = False
            for arg in self._arguments:
                if arg.count("..."):
                    inf = True
                if arg.startswith("["):
                    max += len(arg.split(" "))
                elif not arg == "...":
                    min += 1
                    max += 1
            if not inf and len(self._args) > max:
                raise IndexError("too many arguments, at most", max)
            if len(self._args) < min:
                raise IndexError("too few arguments, needs at least", min)


    def _have_opt(self, opt):
        value = None
        if len(opt) > 1:
            parts = opt.split("=", 1)
            if len(parts) > 1:
                opt, value = parts
            desc = self._long.get(opt)
        else:
            desc = self._opts.get(opt)
        if desc is None:
            raise KeyError("unknown option", f"'{opt}'")
        name, typ, defval, *_ = desc
        if typ == bool:
            self.__dict__[name] += 1
        else:
            if callable(defval):
                value = defval()
            self._set_optarg(opt, desc, value)


    def _set_optarg(self, opt, desc, value):
        if value is None:
            if not self._args:
                raise IndexError(
                    f"not enough arguments: option '{opt}' needs argument")
            value = self._args.pop(0)
        name = desc[0]
        if desc[1] == int:
            try:
                value = int(value)
            except:
                raise TypeError(f"value for '{name}' option must be integer:",
                                repr(value))
        if isinstance(self.__dict__[name], list):
            self.__dict__[name].append(value)
        else:
            self.__dict__[name] = value


    def _help(self):
        print(self._help_message())
        sys.exit()

        
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


    def _usage(self, error="", exit_status=2):
        out = sys.stdout if not exit_status else sys.stderr
        if error:
            print(self._program + ":", error, file=out, end="\n\n")
        print(self._usage_message(), file=out)
        print("run with '-h' to get help on command options", file=out)
        sys.exit(exit_status)


    def _usage_message(self):
        return f"usage: {self._program} [options] {' '.join(self._arguments)}"


    def values(self):
        return { key: val for key, val in self.__dict__.items()
                 if not key.startswith("_") }



def parse(descriptors, args=sys.argv[1:], exit_on_error=True):
    """Parse the command line options according to the specified descriptors.

    Keys of the descriptors dictionary are options or keywords. In case
    of an option, the key is the single option character, and the value
    is a sequence of four or five fields:

      (1) name of the option, used in the returned namespace and as the
      name of the corresponding long option name (after replacing
      underscores with dashes);

      (2) type of the option, which may be bool for options without
      arguments, or str or int for options with an argument of the
      respective type;

      (3) the default value, which can be a starting counter (or False)
      for bool options, or an integer or string value for int or str
      options, respectively, or a list, to which each option argument
      will be appended (for multi-value options);

      (4) the description of the option, for the help text;

      (5) the (optional) name of the option's argument for the help
      text (defaults to 'ARG').

    If the key begins with an underscore, it may be one of these
    keywords:

      "_help_header": a string to print with 'help', between the usage
      and the option explanations;

      "_help_footer": a string to print with 'help', after the option
      explanations;

      "_arguments": a string to print in the usage to describe the
      non-option arguments, or, to check the argument count, a sequence
      with the argument names:
    
         - a normal string counts as one argument towards minimum and
           maximum

         - if it contains '...', there is no maximum the number of
           arguments

         - if it begins with '[', it is optional; if it can be split by
           blanks into multiple words, each one counts toward the
           maximum; e.g. "[param1 param2 param3]" increases the maximum
           by 3, but not the minimum

    If no '?' or 'h' option is specified, they will default to a 'help'
    or a 'usage' function, respectively, which will be called
    immediately when the option is seen. 'help' prints a description of
    the options, framed by the _help_header and the _help_footer;
    'usage' prints a brief summary of the program's parameters. Both
    terminate the program after printing the message. (This behaviour
    can be deactivated by setting a '-h' and/or a '-?' option.)

    In case of a normal return of the parse() function (i.e. options and
    number of arguments okay, or exit_on_error passed as false), it
    returns an OptionValueContainer and the remaining command line
    arguments. Example:

      ovc, args = pgetopt.parse({
      # opt: (name,          type, default value, helptext[, arg name])
        "s": ("schmooze",    bool, 0,    "increase schmooziness"),
        "o": ("output_file", str,  None, "output file (or stdout)", "NAME"),
        "n": ("repetitions", int,  3,    "number of repetitions"),
        "d": ("debug",       str, [],    "debug topics", "DEBUG_TOPIC"),
      # keyword:        value
        "_arguments":   ("string_to_print", "..."),
        "_help_header": "print a string a number of times",
        "_help_footer": "This is just an example program.",
      }

      On return, ovc has the following fields:
        ovc.verbose: the number of -s options counted,
        ovc.output_file: the parameter of -o or --output-file, or None
        ovc.repetitions: the parameter of -n or --repetitions, or 3
        ovc.debug: a list with all parameters given to -d or --debug

    Parameters to int or str options are taken from the next argument;
    with long options, "--option=parameter" is also possible.

    Other potentially useful fields of ovc:
      ovc._help(),
      ovc._usage(): the help and usage function, respectively
    
      ovc._help_message(),
      ovc._usage_message(): the corresponding messages as strings

    """
    ovc = OptionValueContainer(descriptors, args)
    try:
        ovc._parse()
        return ovc, ovc._args
    except Exception as e:
        if exit_on_error:
            ovc._usage(" ".join(map(str, e.args)), exit_status=1)
        raise(e)

# EOF
