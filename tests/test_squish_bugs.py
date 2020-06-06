#!/usr/bin/env python3

from pgetopt import parse
import unittest

# test cases to reproduce bugs found

class BugsTestCase(unittest.TestCase):

    def test_emptyDesc(self):
        """does it work without any options or keywords?"""
        ovc, args = parse({}, [], exit_on_error=False)
        self.assertEqual(ovc.ovc_values(), {})
        self.assertEqual(args, [])

    def test_emptyOpts(self):
        """does it work without any options but _arguments?"""
        ovc, args = parse({ "_arguments": "arg1 ..." },
                          [], exit_on_error=False)
        self.assertEqual(ovc.ovc_values(), {})
        self.assertEqual(args, [])

