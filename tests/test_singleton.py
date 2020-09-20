#!/usr/bin/env python3

import jpylib as y

import unittest

class Token(metaclass=y.Singleton):
    def __init__(self, name):
        self.name = name


class TemplateTestcase(unittest.TestCase):

    def test_equal(self):
        t1 = Token("foo")
        t2 = Token("bar")
        self.assertIs(t1, t2)
        self.assertEqual(t1.name, t2.name)
        # print()
        # print("t1.name =", repr(t1.name))
        # print("t2.name =", repr(t2.name))

