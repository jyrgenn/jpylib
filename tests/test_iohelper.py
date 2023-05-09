#!/usr/bin/env python3

import jpylib as y

import os
import re
import sys
import unittest
import collections

files = ["examples/testdata/input_lines_a",
         "examples/testdata/input_lines_b"]
nonex = ["examples/testdata/input_lines_a",
         "examples/testdata/input_lines_nonex"]
fstdin = "examples/testdata/input_lines_stdin"

mapfile = "lib/mapping"
mapfile_c = "lib/mapping.comments"
dnsfile = "lib/dnszone"
dnsfile_b = "lib/dnszone.botched"


def read_map(fname, sep=None, comments_re="^\\s*#", skip_fails=False):
    result = {}
    with open(fname) as f:
        for line in f:
            if comments_re and re.search(comments_re, line):
                continue
            line = line.strip()
            if not line:
                continue
            try:
                key, value = line.split(sep, 1)
                result[key] = value
            except Exception as e:
                if skip_fails:
                    pass
                else:
                    raise e
    return result


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


class ReadItemsTestcase(unittest.TestCase):

    def test_read_items_defaults(self):
        expect = "one two three five seven nine ten".split()
        fname = "lib/items"
        result = list(y.read_items(fname))
        # y.debug("result", result)
        self.assertEqual(result, expect)

    def test_read_items_no_empty(self):
        expect = ["one",
                  "two",
                  "three",
                  "five",
                  "seven",
                  "",
                  "nine",
                  "ten",
                  "",
                  "",
                  ]
        fname = "lib/items"
        result = list(y.read_items(fname, skip_empty=False))
        # y.debug("result", result)
        self.assertEqual(result, expect)

    def test_read_items_lstrip(self):
        expect = "one,,,, two three five seven nine,,,, ten".split()
        fname = "lib/items.left"
        result = list(y.read_items(fname, lstrip=",."))
        # y.debug("result", result)
        self.assertEqual(result, expect)

    def test_read_items_no_lstrip(self):
        expect = [" one",
                  "  two",
                  " three",
                  "five",
                  "seven",
                  "nine",
                  "ten",
                  ]    
        fname = "lib/items"
        result = list(y.read_items(fname, lstrip=False))
        # y.debug("result", result)
        self.assertEqual(result, expect)

    def test_read_items_rstrip(self):
        expect = ",one ,.,two ,three five seven ..nine ten".split()
        expect.insert(4, ',,.,,,,,,# no six (space indented)')
        fname = "lib/items.left"
        result = list(y.read_items(fname, rstrip=",.\t"))
        # y.debug("result", result)
        self.assertEqual(result, expect)

    def test_read_items_no_rstrip(self):
        expect = ["one    ",
                  "two	",
                  "three",
                  "five",
                  "seven",
                  "nine    ",
                  "ten",
                  ]    
        fname = "lib/items"
        result = list(y.read_items(fname, rstrip=False))
        # y.debug("result", result)
        self.assertEqual(result, expect)

    def test_read_items_no_rstrip_no_comments(self):
        expect = ["# This is a test file for read_items()",
                  "one    ",
                  "two	",
                  "three",
                  "# no four (tab indented)",
                  "five",
                  "# no six (space indented)",
                  "seven",
                  "nine    ",
                  "ten",
                  "# EOF",
]    
        fname = "lib/items"
        result = list(y.read_items(fname, rstrip=False, comments_re=False))
        # y.debug("result", result)
        self.assertEqual(result, expect)

    def test_read_items_no_rstrip_no_newline(self):
        expect = ["one    \n",
                  "two	\n",
                  "three\n",
                  "five\n",
                  "seven\n",
                  "nine    \n",
                  "ten\n",
                  ]    
        fname = "lib/items"
        result = list(y.read_items(fname, rstrip=False, strip_newline=False))
        # y.debug("result", result)
        self.assertEqual(result, expect)

    def test_read_items_other_comment(self):
        expect = ["# This is a test file for read_items()",
                  "one",
                  "two",
                  "three",
                  "five",
                  "/ no six (space indented)",
                  "seven",
                  "nine",
                  "ten",
                  "# EOF",
                  ]    
        fname = "lib/items.comments"
        result = list(y.read_items(fname, comments_re="//"))
        # y.debug("result", result)
        self.assertEqual(result, expect)


    def test_read_mapping(self):
        themap = read_map(mapfile)
        tested = y.read_mapping(mapfile)
        self.assertEqual(themap, tested)

    def test_read_mapping_comments(self):
        themap = read_map(mapfile_c)
        tested = y.read_mapping(mapfile)
        self.assertEqual(themap, tested)

    def test_read_mapping_no_comments(self):
        themap = read_map(mapfile_c, comments_re=None)
        tested = y.read_mapping(mapfile)
        self.assertNotEqual(themap, tested)

    def test_read_mapping_other_comment(self):
        themap = read_map(dnsfile, comments_re="^\\s*;;")
        tested = y.read_mapping(dnsfile, comments_re="^\\s*;;")
        self.assertEqual(themap, tested)

    def test_read_mapping_no_skip(self):
        with self.assertRaises(ValueError):
            themap = read_map(dnsfile_b, comments_re="^\\s*;;")
        with self.assertRaises(ValueError):
            tested = y.read_mapping(dnsfile_b, comments_re="^\\s*;;")

    def test_read_mapping_skip(self):
        themap = read_map(dnsfile_b, comments_re="^\\s*;;",
                          skip_fails=True)
        tested = y.read_mapping(dnsfile_b, comments_re="^\\s*;;",
                                skip_fails=True)
        self.assertEqual(themap, tested)

