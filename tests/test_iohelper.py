#!/usr/bin/env python3

import jpylib as y

import os
import sys
import unittest
import collections

files = ["examples/testdata/input_lines_a",
         "examples/testdata/input_lines_b"]
nonex = ["examples/testdata/input_lines_a",
         "examples/testdata/input_lines_nonex"]
fstdin = "examples/testdata/input_lines_stdin"

class IOHelperTestcase(unittest.TestCase):

    def setUp(self):
        pass

    def test_input_lines_files(self):
        result = ["a", "bb", "ccc", "dddd", "eeeee", "ffffff",
                  "1: 6235", "2: 13152", "3: 18136", "4: 6486",
                  "5: 14862", "6: 6679", ]
        self.assertEqual(list(map(str.strip, y.all_input_lines(files))),
                         result)

    def test_input_lines_stdin_a(self):
        # w/ no args
        result = ["prplfrps\n"]
        with open(fstdin) as stdin:
            with y.inputFrom(stdin):
                data = list(y.all_input_lines())
        self.assertEqual(data, result)

    def test_input_lines_stdin_b(self):
        # w/ empty args list
        result = ["prplfrps\n"]
        with open(fstdin) as stdin:
            with y.inputFrom(stdin):
                data = list(y.all_input_lines([]))
        self.assertEqual(data, result)

    def test_input_lines_nonex(self):
        with self.assertRaises(FileNotFoundError) as err:
            data = list(map(str.strip, y.all_input_lines(nonex)))
        
        
    def test_input_lines_continue(self):
        result = ["a", "bb", "ccc", "dddd", "eeeee", "ffffff",]
        sys.argv[0] = "the_program"
        with y.outputCaptured() as (out, err):
            data = list(map(str.strip, y.all_input_lines(nonex, True)))
        self.assertEqual(data, result)
        self.assertEqual(err.getvalue(),
                         "the_program: [Errno 2] No such file or directory: 'examples/testdata/input_lines_nonex'\n")
        
    def test_input_lines_handler(self):
        result = ["a", "bb", "ccc", "dddd", "eeeee", "ffffff",]
        handler_run = None

        def handler(fname, e):
            nonlocal handler_run
            handler_run = "handled " + fname
            self.assertIsInstance(e, FileNotFoundError)

        data = list(map(str.strip, y.all_input_lines(nonex, handler)))
        self.assertEqual(data, result)
        self.assertEqual(handler_run,
                         "handled examples/testdata/input_lines_nonex")
