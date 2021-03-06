#!/usr/bin/env python3

from jpylib.pgetopt import parse
import unittest

# test with different styles of option argument passing

optdescs = {
    "o": ("option", int, 1, "option with argument"),
    "_arguments": [],
}

class OptargTestcase(unittest.TestCase):

    def test_short_next(self):
        """short option, next arg"""
        ovc, args = parse(optdescs, ["-o", "4"], exit_on_error=False)
        self.assertEqual(ovc.ovc_values(), dict(option=4))

    def test_short_same(self):
        """short option, same arg"""
        ovc, args = parse(optdescs, ["-o4"], exit_on_error=False)
        self.assertEqual(ovc.ovc_values(), dict(option=4))

    def test_long_next(self):
        """long option, next arg"""
        ovc, args = parse(optdescs, ["--option", "4"], exit_on_error=False)
        self.assertEqual(ovc.ovc_values(), dict(option=4))

    def test_long_same(self):
        """long option, same arg"""
        ovc, args = parse(optdescs, ["--option=4"], exit_on_error=False)
        self.assertEqual(ovc.ovc_values(), dict(option=4))

