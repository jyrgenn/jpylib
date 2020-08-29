#!/usr/bin/env python3

import jpylib as y
from jpylib import *

import unittest

class TerminalTestcase(unittest.TestCase):

    def setUp(self):
        sizes = y.backquote("stty size < /dev/tty").split()
        self.rows = int(sizes[0])
        self.cols = int(sizes[1])

    def test_null(self):
        # trigger setUp()
        self.assertEqual(True, True)

# removed terminal_size() test cases due to its lack of existance, now
