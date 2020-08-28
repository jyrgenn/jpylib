#!/usr/bin/env python3

import jpylib as y
import unittest

trues = "yes y sure ja j jou si on t true  aye 1 affirmative"
falses = "no n nope nein nee   off f false nay 0 negative"
bullsh = "do da di  sdf sdf fs df gdfssaxs dcsgdv fd"

class BoolishTestcase(unittest.TestCase):

    def setUp(self):
        pass

    def test_true(self):
        for word in trues.split():
            self.assertTrue(y.boolish(word))

    def test_false(self):
        for word in falses.split():
            self.assertFalse(y.boolish(word))

    def test_raises(self):
        for word in bullsh.split():
            with self.assertRaises(ValueError):
                y.boolish(word)

    def test_default(self):
        for word in bullsh.split():
            self.assertEqual(y.boolish(word, default="gronz"), "gronz")


class FlattenTestcase(unittest.TestCase):

    def setUp(self):
        pass

    def test_flatten_0(self):
        """non-list non-string argument"""
        self.assertEqual(list(y.flatten(4)), [4])

    def test_flatten_0a(self):
        """non-list string argument"""
        self.assertEqual(list(y.flatten("abc")), ["abc"])

    def test_flatten_1(self):
        """list with single non-string element"""
        self.assertEqual(list(y.flatten([4])), [4])

    def test_flatten_1a(self):
        """list with single string element"""
        self.assertEqual(list(y.flatten(["abc"])), ["abc"])

    def test_flatten_2(self):
        """tuple with two non-string elements"""
        self.assertEqual(list(y.flatten((4, 5))), [4, 5])

    def test_flatten_2a(self):
        """tuple with two string elements"""
        self.assertEqual(list(y.flatten(("abc", "def"))), ["abc", "def"])

    def test_flatten_n(self):
        """tuple with quite a number of string elements"""
        self.assertEqual(list(y.flatten((
            "abc", "def", "ghi", "jkl", "mno", "pqr", "stu", "vwx", "yzß"
            ))), [
                "abc", "def", "ghi", "jkl", "mno", "pqr", "stu", "vwx", "yzß"
                ])
        
    def test_flatten_nested(self):
        """nested tuple with quite a number of string elements"""
        self.assertEqual(list(y.flatten((
            [], "abc", ["def", "ghi"], ("jkl"), [(["mno"], "pqr"),
                                                     "stu", "vwx"], "yzß"
            ))), [
                "abc", "def", "ghi", "jkl", "mno", "pqr", "stu", "vwx", "yzß"
            ])
        
