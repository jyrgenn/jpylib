#!/usr/bin/env python3

import jpylib as y
import unittest


avg_data = [24289, 22071, 6436, 22019, 10069, 13505, 17707, 20720, 11461,
            19624, 1990, 2416, 2374, 17237, 1947, 25304, 29098, 8972, 28219,
            1269, 1162, 11021, 3083, 3968, 32278, 1390]
avg_d_so = [24289, 22071, 6436, 22019, 10069, 13505, 17707, 20720, 11461,
            19624, 1990, 2416, 2374, 17237, 1947, 25304, 29098, 8972, 28219,
            1269, 11021, 3083, 3968, 1390]
avg_d_mr = (1162 + 32278) / 2


class averageTestcase(unittest.TestCase):

    def test_remove_outliers(self):
        self.assertEqual(y.remove_outliers(avg_data), avg_d_so)

    def test_midrange(self):
        self.assertEqual(y.avg_midrange(avg_data), avg_d_mr)

class IntTestcase(unittest.TestCase):

    pairs = ((" ", None), ("23", 23), (" 23", 23), ("23x", None), ([], None), 
             ({}, None), ("25.6", None), ("25,6", None), ("0", 0), ("+42", 42),
             (" -42", -42), ("-1", -1), ("", None),
    )

    def test_maybe_int(self):
        """maybe_int on all pairs"""
        for arg, value in self.pairs:
            self.assertEqual(y.maybe_int(arg), value)

    def test_is_int(self):
        """is_int on all pairs"""
        for arg, value in self.pairs:
            self.assertEqual(y.is_int(arg), value is not None)
        
              
class NumTestcase(unittest.TestCase):

    pairs = ((" ", None), ("23", 23), (" 23", 23), ("23x", None), ([], None), 
             ({}, None), ("25.6", 25.6), ("25,6", None), ("0", 0), ("+42", 42),
             (" -42", -42), ("-1", -1), ("", None),
             ("23.4", 23.4), (" 23.4", 23.4), ("23e1", 230), ("25.6", 25.6),
             ("25,6", None), ("0", 0), ("+42.1", 42.1),
             (" -42.0", -42), ("-1", -1),
    )

    def test_maybe_num(self):
        """maybe_int on all pairs"""
        for arg, value in self.pairs:
            self.assertEqual(y.maybe_num(arg), value)

    def test_is_num(self):
        """is_int on all pairs"""
        for arg, value in self.pairs:
            self.assertEqual(y.is_num(arg), value is not None)
        
              
