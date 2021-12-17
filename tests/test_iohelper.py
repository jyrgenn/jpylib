#!/usr/bin/env python3

import jpylib as y

import os
import unittest
import collections

class IOHelperTestcase(unittest.TestCase):

    def setUp(self):
        pass

    def test_input_lines_files(self):
        result = ["a", "bb", "ccc", "dddd", "eeeee", "ffffff",
                  "1: 6235", "2: 13152", "3: 18136", "4: 6486",
                  "5: 14862", "6: 6679", ]
        dir = "examples/testdata"
        files = ["input_lines_a", "input_lines_b"]
        testdata = map(lambda f: os.path.join(dir, f), files)
        self.assertEqual(list(map(str.strip, y.all_input_lines(testdata))),
                         result)

    def test_input_lines_stdin(self):
        result = ["prplfrps\n"]
        data = list(y.all_input_lines([]))
        self.assertEqual(data, result)


        
