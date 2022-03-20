#!/usr/bin/env python3

import jpylib as y
import unittest
import collections

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
        

class SequenceTestcase(unittest.TestCase):

    def test_isseq_0(self):
        self.assertTrue(y.is_sequence([]))

    def test_isseq_1(self):
        self.assertFalse(y.is_sequence(set()))

    def test_isseq_2(self):
        self.assertFalse(y.is_sequence(3))

    def test_isseq_3(self):
        self.assertFalse(y.is_sequence("blabla"))

    def test_isseq_4(self):
        self.assertTrue(y.is_sequence((3, 4, 5)))

    def test_isseq_5(self):
        self.assertTrue(y.is_sequence(collections.deque([3, 4, 5])))

    def test_isseq_6(self):
        self.assertTrue(y.is_sequence(collections.UserList([3, 4, 5])))

    def test_isseq_7(self):
        self.assertFalse(y.is_sequence({}))

    def test_isseq_8(self):
        self.assertFalse(y.is_sequence(collections.UserString(5)))

    def test_isseq_9(self):
        self.assertTrue(y.is_sequence(range(22)))

    def test_isseq_es(self):
        self.assertFalse(y.is_sequence(""))
        

class IdentityTestcase(unittest.TestCase):

    def test_identity_0(self):
        self.assertEqual(1, y.identity(1))

    def test_identity_1(self):
        self.assertEqual("lala", y.identity("lala"))

    def test_identity_2(self):
        self.assertEqual(y.identity, y.identity(y.identity))

    def test_identity_3(self):
        obj1 = { 3, 4, 5, 6 }
        self.assertEqual(id(obj1), id(y.identity(obj1)))
        
