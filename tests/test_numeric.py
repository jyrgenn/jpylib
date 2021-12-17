#!/usr/bin/env python3

import jpylib as y
import unittest


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
        
              
