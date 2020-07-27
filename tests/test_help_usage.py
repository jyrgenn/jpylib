#!/usr/bin/env python3

import unittest
from jpylib.pgetopt import parse
from capture import outputAndExitCaptured

# test replacing the default usage message

class UsageTestcase(unittest.TestCase):

    def test_usage0(self):
        """test usage output 0 args to err"""
        ovc, args = parse({
            "v": ("verbose", bool, 1, "increase verbosity"),
            "z": ("zounds", int, 1, "number of zounds"),
            "_arguments": [],
        }, ["-v"])
        with outputAndExitCaptured() as (out, err, status):
            ovc.ovc_usage()
        self.assertEqual(out.getvalue(), "")
        self.assertEqual(err.getvalue().rstrip(),
                         """usage: {} [options]
use '-h' option to get help on options""".format(ovc._program))
        self.assertEqual(status.value, 64)


    def test_usage1(self):
        """test usage output 0 args, to err, other exit status"""
        ovc, args = parse({
            "v": ("verbose", bool, 1, "increase verbosity"),
            "z": ("zounds", int, 1, "number of zounds"),
            "_arguments": [],
        }, ["-v"])
        with outputAndExitCaptured() as (out, err, status):
            ovc.ovc_usage(exit_status=63)
        self.assertEqual(out.getvalue(), "")
        self.assertEqual(err.getvalue().rstrip(),
                         """usage: {} [options]
use '-h' option to get help on options""".format(ovc._program))
        self.assertEqual(status.value, 63)

    def test_usage2(self):
        """test usage output 0 args, to err, message, other exit status"""
        ovc, args = parse({
            "v": ("verbose", bool, 1, "increase verbosity"),
            "z": ("zounds", int, 1, "number of zounds"),
            "_arguments": [],
        }, ["-v"])
        with outputAndExitCaptured() as (out, err, status):
            ovc.ovc_usage("sis is rong", exit_status=63)
        self.assertEqual(out.getvalue(), "")
        self.assertEqual(err.getvalue().rstrip(),
                         """{}: sis is rong

usage: {} [options]
use '-h' option to get help on options""".format(ovc._program, ovc._program))
        self.assertEqual(status.value, 63)

    def test_usage3(self):
        """test usage output 0 args, to err, message"""
        ovc, args = parse({
            "v": ("verbose", bool, 1, "increase verbosity"),
            "z": ("zounds", int, 1, "number of zounds"),
            "_arguments": [],
        }, ["-v"])
        with outputAndExitCaptured() as (out, err, status):
            ovc.ovc_usage("sis is rong")
        self.assertEqual(out.getvalue(), "")
        self.assertEqual(err.getvalue().rstrip(),
                         """{}: sis is rong

usage: {} [options]
use '-h' option to get help on options""".format(ovc._program, ovc._program))
        self.assertEqual(status.value, 64)

    def test_usage4(self):
        """test usage output 0 args, to stdout, no message"""
        ovc, args = parse({
            "v": ("verbose", bool, 1, "increase verbosity"),
            "z": ("zounds", int, 1, "number of zounds"),
            "_arguments": [],
        }, ["-v"])
        with outputAndExitCaptured() as (out, err, status):
            ovc.ovc_usage(exit_status=0)
        self.assertEqual(err.getvalue(), "")
        self.assertEqual(out.getvalue().rstrip(),
                         """usage: {} [options]
use '-h' option to get help on options""".format(ovc._program))
        self.assertEqual(status.value, 0)

    def test_usage5(self):
        """test usage output 3 args, to stdout, no message"""
        ovc, args = parse({
            "v": ("verbose", bool, 1, "increase verbosity"),
            "z": ("zounds", int, 1, "number of zounds"),
            "_arguments": ["1", "2", "drei"],
        }, ["-v", "hahaha", "hihihi", "hohoho"])
        with outputAndExitCaptured() as (out, err, status):
            ovc.ovc_usage(exit_status=0)
        self.assertEqual(err.getvalue(), "")
        self.assertEqual(out.getvalue().rstrip(),
                         """usage: {} [options] 1 2 drei
use '-h' option to get help on options""".format(ovc._program))
        self.assertEqual(status.value, 0)


class HelpTestcase(unittest.TestCase):

    def test_help_msg(self):
        """Test help message."""
        ovc, args = parse({
            # opt: (name,        type, default value, helptext[, arg name])
            "s": ("schmooze",    bool, 0,    "more schmooziness"),
            "o": ("output_file", str,  None, "output file (or stdout)", "NAME"),
            "n": ("repetitions", int,  3,    "number of repetitions"),
            "d": ("debug",       str, [],    "debug topics", "DEBUG_TOPIC"),
            # keyword:        value
            "_arguments":   ["string_to_print", "..."],
            "_help_header": "print a string a number of times",
            "_help_footer": "This is just an example program.",
            "_program": "schmooze",
        }, ["gnaddel"])
        self.assertEqual(ovc.ovc_help_msg(),
                         """usage: schmooze [options] string_to_print ...
print a string a number of times

 -?, --usage 
    show usage briefly
 -d, --debug DEBUG_TOPIC
    debug topics (str arg, default [])
 -h, --help 
    show help on options
 -n, --repetitions ARG
    number of repetitions (int arg, default 3)
 -o, --output-file NAME
    output file (or stdout) (str arg, default None)
 -s, --schmooze 
    more schmooziness

This is just an example program.""")

    def test_help_out(self):
        """Test help message with -h."""
        with outputAndExitCaptured() as (out, err, status):
            ovc, args = parse({
                # opt: (name,        type, default value, helptext[, arg name])
                "s": ("schmooze",    bool, 0,    "more schmooziness"),
                "o": ("output_file", str,  None, "output file (or stdout)", "NAME"),
                "n": ("repetitions", int,  3,    "number of repetitions"),
                "d": ("debug",       str, [],    "debug topics", "DEBUG_TOPIC"),
                # keyword:        value
                "_arguments":   ["string_to_print", "..."],
                "_help_header": "print a string a number of times",
                "_help_footer": "This is just an example program.",
                "_program": "schmooze",
                }, ["-h"], exit_on_error=False)
        self.assertEqual(err.getvalue(), "")
        self.assertEqual(status.value, 0)
        self.assertEqual(out.getvalue(),
                         """usage: schmooze [options] string_to_print ...
print a string a number of times

 -?, --usage 
    show usage briefly
 -d, --debug DEBUG_TOPIC
    debug topics (str arg, default [])
 -h, --help 
    show help on options
 -n, --repetitions ARG
    number of repetitions (int arg, default 3)
 -o, --output-file NAME
    output file (or stdout) (str arg, default None)
 -s, --schmooze 
    more schmooziness

This is just an example program.
""")


    def test_called_help(self):
        """Test called ovc_help()."""
        with outputAndExitCaptured() as (out, err, status):
            ovc, args = parse({
                # opt: (name,        type, default value, helptext[, arg name])
                "s": ("schmooze",    bool, 0,    "more schmooziness"),
                "o": ("output_file", str,  None, "output file (or stdout)", "NAME"),
                "n": ("repetitions", int,  3,    "number of repetitions"),
                "d": ("debug",       str, [],    "debug topics", "DEBUG_TOPIC"),
                # keyword:        value
                "_arguments":   ["string_to_print", "..."],
                "_help_header": "print a string a number of times",
                "_help_footer": "This is just an example program.",
                "_program": "schmooze",
                }, ["narg"], exit_on_error=False)
            ovc.ovc_help()
        self.assertEqual(err.getvalue(), "")
        self.assertEqual(status.value, 0)
        self.assertEqual(out.getvalue(),
                         """usage: schmooze [options] string_to_print ...
print a string a number of times

 -?, --usage 
    show usage briefly
 -d, --debug DEBUG_TOPIC
    debug topics (str arg, default [])
 -h, --help 
    show help on options
 -n, --repetitions ARG
    number of repetitions (int arg, default 3)
 -o, --output-file NAME
    output file (or stdout) (str arg, default None)
 -s, --schmooze 
    more schmooziness

This is just an example program.
""")

