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

