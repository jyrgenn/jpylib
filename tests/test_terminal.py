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

    def test_size(self):
        self.assertEqual(terminal_size(), (self.cols, self.rows))

    def test_fd0(self):
        self.assertEqual(terminal_size(0), (self.cols, self.rows))

    def test_fd1(self):
        self.assertEqual(terminal_size(1), (self.cols, self.rows))
        
    def test_fd2(self):
        self.assertEqual(terminal_size(2), (self.cols, self.rows))

    def test_fd3(self):
        self.assertEqual(terminal_size(3), (None, None))

    def test_fd4(self):
        self.assertEqual(terminal_size(4), (None, None))

