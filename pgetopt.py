#!/usr/bin/env python3

import os
import sys
import copy
from collections.abc import Iterable

debug = True

class OptionValueContainer:
    def __init__(self, descriptors):
        """The argument is a dict with optchar as key, descriptor as value.

        The option descriptor is a tuple with the name, type (bool
        (argument-less, also counts), int (with int arg), str (with str arg)),
        default value, and help text; optional an argument name. The name will
        be the name in the OVCs name space, and also the long option name (with
        underscores replaced by dashes(.

        """
        self._program = os.path.basename(sys.argv[0])
        self._opts = descriptors
        print(self)
        for opt, desc in descriptors.items():
            if opt.startswith("_"):
                continue                # allow for _<keyword> entries
            assert isinstance(desc, Iterable) and len(desc) in (4, 5),\
                f"descriptor of option '{opt}' not iterable len 4 or 5"
            assert isinstance(desc[0], str),\
                f"name of option '{opt}' not a string"
            assert desc[1] in (bool, int, str),\
                f"invalid type option '{opt}': {desc[1]}"
        if "h" not in self._opts:
            self._opts["h"] = ("help", self._help, None, "show help on options")
        if "?" not in self._opts:
            self._opts["?"] = ("usage", self._usage, None, "show usage briefly")
        self._arguments = self._opts.get("_arguments", "")
        self._help_header = self._opts.get("_help_header", "")
        self._help_footer = self._opts.get("_help_footer", "")
        self._long = { desc[0] : desc for desc in self._opts.values() }
        for desc in self._opts.values():
            if not isinstance(desc, str):
                self.__dict__[desc[0]] = desc[2]
        print(self)

    def __str__(self):
        """Return a string representation of the OptionValueContainer."""
        sep = "\n    " if debug else ""
        return self.__class__.__name__ + "(" + sep + (", " + sep).join(
            [f"{k}={repr(self.__dict__[k])}" for k in sorted(self.__dict__)])\
            + sep + ")"


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
        return self, self._args


    def _have_option(self, opt, is_long_option):
        value = None
        if is_long_option:
            parts = opt.split("=", 1)
            if len(parts) > 1:
                opt, value = parts
        if opt not in self._opts:
            raise KeyError(f"{self._program}: unknown option '-{opt}'")
        name, typ, *_ = self._opts[opt]
        if typ == bool:
            self.__dict__[name] += 1
        elif typ in (str, int):
            self._set_optarg(opt, value)
        elif callable(typ):
            typ()
                
        
    def _set_optarg(self, opt, value):
        if value is None:
            value = self._args.pop(0)
        if self._opts[opt][1] == int:
            value = int(value)
        if isinstance(self.__dict__[self._opts[opt][0]], list):
            self.__dict__[self._opts[opt][0]].append(value)
        else:
            self.__dict__[self._opts[opt][0]] = value


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
            msg += f" -{opt}, --{desc[0].replace('_', '-')} {arg}\n    {desc[3]}"
            if desc[1] in (int, str):
                msg += f" ({desc[1].__name__} arg, default: {repr(desc[2])})"
            msg += "\n"
        if self._help_footer:
            msg += "\n" + self._help_footer
        return msg

    def _usage(self, exit_status=0):
        print(self._usage_message(),
              file=sys.stdout if not exit_status else sys.stderr)
        sys.exit(exit_status)

    def _usage_message(self):
        return f"usage: {self._program} [options] {self._arguments}"



def parse(descriptors, args=sys.argv[1:], exit_on_error=True):
    """Parse the command line options according to the passed descriptors.
    """
    try:
        return OptionValueContainer(descriptors)._parse(args)
    except Exception as e:
        if exit_on_error:
            sys.exit(e.args)
        raise(e)


if __name__ == "__main__":
    ovc, args = parse({
        "_arguments": "[arg1 ...]",
#        "_help_header": "test the option parser",
#        "_help_footer": "if you like this, buy me a beer",
        "q": ("quiet", bool, False, "keep quiet (error output only)"),
        "v": ("verbose", bool, 1, "increase verbosity"),
        "f": ("input_file", str, "/dev/stdin", "name of input file", "PATHNAME"),
    }, exit_on_error=False)
    print(ovc)
