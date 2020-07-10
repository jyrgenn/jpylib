#!/usr/bin/env python3

from jpylib.pgetopt import parse
import unittest

# test replacing the default help/usage options

help_called = False

def my_help():
    global help_called
    help_called = True
    return 6

class HelpTestcase(unittest.TestCase):

    def test_hounds(self):
        """-h/--hounds option"""
        ovc, args = parse({
            "v": ("verbose", bool, 1, "increase verbosity"),
            "h": ("hounds", int, 1, "number of hounds"),
            "_arguments": [],
        }, ["-vh5"], exit_on_error=False)
        self.assertEqual(ovc.ovc_values(), dict(verbose=2, hounds=5))

    def test_help_int5(self):
        """-h/--help option"""
        ovc, args = parse({
            "v": ("verbose", bool, 1, "increase verbosity"),
            "h": ("help", int, 1, "number of hounds"),
            "_arguments": [],
        }, ["-v", "--help=5"], exit_on_error=False)
        self.assertEqual(ovc.ovc_values(), dict(verbose=2, help=5))

    def test_help_def(self):
        """-h/--help default"""
        ovc, args = parse({
            "v": ("verbose", bool, 1, "increase verbosity"),
            "h": ("help", int, 1, "number of hounds"),
            "_arguments": [],
        }, ["-v"], exit_on_error=False)
        self.assertEqual(ovc.ovc_values(), dict(verbose=2, help=1))

    def test_help_bool(self):
        """-h/--help option"""
        ovc, args = parse({
            "v": ("verbose", bool, 1, "increase verbosity"),
            "h": ("help", bool, 1, "number of hounds"),
            "_arguments": [],
        }, ["-v", "--help"], exit_on_error=False)
        self.assertEqual(ovc.ovc_values(), dict(verbose=2, help=2))

    def test_help_func(self):
        """call help function"""
        ovc, args = parse({
            "v": ("verbose", bool, 1, "increase verbosity"),
            "h": ("help", my_help, None, "number of hounds"),
            "_arguments": [],
        }, ["-v", "--help"], exit_on_error=False)
        self.assertEqual(ovc.ovc_values(), dict(verbose=2, help=6))
        self.assertTrue(help_called)
        
    def test_usage_short0(self):
        """own usage option 0"""
        ovc, args = parse({
            "v": ("verbose", bool, 1, "increase verbosity"),
            "?": ("usage", bool, False, "opposite of overly"),
            "_arguments": [],
        }, ["-v", "-?"], exit_on_error=False)
        self.assertEqual(ovc.ovc_values(), dict(verbose=2, usage=1))

    def test_usage_short1(self):
        """own usage option 1"""
        ovc, args = parse({
            "v": ("verbose", bool, 1, "increase verbosity"),
            "?": ("usage", int, 2, "opposite of overly"),
            "_arguments": [],
        }, ["-v", "--usage", "4"], exit_on_error=False)
        self.assertEqual(ovc.ovc_values(), dict(verbose=2, usage=4))

    def test_usage_short2(self):
        """own usage option 2"""
        ovc, args = parse({
            "v": ("verbose", bool, 1, "increase verbosity"),
            "?": ("usage", int, 2, "opposite of overly"),
            "_arguments": [],
        }, ["-v"], exit_on_error=False)
        self.assertEqual(ovc.ovc_values(), dict(verbose=2, usage=2))

