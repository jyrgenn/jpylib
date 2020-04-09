#!/usr/bin/env python3

import os
import sys
import copy
import collections.abc


class OptionValueContainer:
    def __init__(self, descriptors):
        """Init. The descriptors is a dict with optchar as key, descriptor as value.

        The option descriptor is the name, type, default value, and help text.
        """
        self._program = os.path.basename(sys.argv[0])
        self._opts = self._copy_desc(descriptors)
        for desc in self._opts.values():
            self.__dict__[desc[0]] = desc[2]

    def __str__(self):
        return self.__class__.__name__ + "(" + ", ".join(
            [f"{k}={repr(self.__dict__[k])}" for k in sorted(self.__dict__)]) + ")"


    def _copy_desc(self, descriptors):
        """Check and copy the descriptors."""
        result = {}
        for opt, desc in descriptors.items():
            result[opt] = desc
            if isinstance(desc, str):
                continue
            assert isinstance(desc, collections.abc.Iterable) and len(desc) == 4,\
                f"descriptor of option '{opt}' not iterable len 4"
            assert isinstance(desc[0], str), f"name of option '{opt}' not a string"
            assert desc[1] in (bool, int, str), f"invalid type option '{opt}': {desc[1]}"
            result["-" + desc[0].replace("_", "-")] = desc # --long-option
        for h_opt in "h", "-help":
            if h_opt not in result:
                result[h_opt] = ("help", self._help, None, "show help on options")
        if '?' not in result:
            result['?'] = ("usage", self._usage, None, "show brief usage info")
        return result


    def _parse(self, args):
        self._args = args
        while self._args and self._args[0].startswith("-"):
            arg = self._args.pop(0)
            if arg == "--":
                break
            if arg.startswith("--"):
                self._have_option(arg[1:])
            else:
                for c in arg[1:]:
                    self._have_option(c)
        return self, self._args


    def _have_option(self, opt):
        if opt not in self._opts:
            raise KeyError(f"{self._program}: unknown option '-{opt}'")
        name, typ, *_ = self._opts[opt]
        if typ == bool:
            self.__dict__[name] += 1
        elif typ in (str, int):
            self._set_optarg(opt)
        elif callable(typ):
            typ()
                
        
    def _set_optarg(self, opt):
        value = self._args.pop(0)
        if self._opts[opt][1] == int:
            value = int(value)
        if isinstance(self.__dict__[self._opts[opt][0]], list):
            self.__dict__[self._opts[opt][0]].append(value)
        else:
            self.__dict__[self._opts[opt][0]] = value


    def _help(self):
        print(self._program + ":", self._opts.get("_purpose", ""))
        for opt in sorted(self._opts.keys()):
            if opt.startswith("_"):
                continue
            sep = " "
            if len(opt) > 1:
                sep = "\n    " + sep
            desc = self._opts[opt]
            print(f" -{opt}:{sep}{desc[3]}", end="")
            if desc[1] in (int, str):
                print(f" ({desc[1].__name__} arg, default: {repr(desc[2])})", end="")
            print()
        sys.exit()

    def _usage(self):
        sys.exit("usage method")



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
        "_purpose": "test the option parser",
        "f": ("input_file", str, "/dev/stdin", "name of input file"),
    }, exit_on_error=False)
    print(ovc)
