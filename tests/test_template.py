#!/usr/bin/env python3

import jpylib as y

import unittest

class TemplateTestcase(unittest.TestCase):

    def setUp(self):
        pass

    def test_equal(self):
        self.assertEqual(3+4, 7)

    def test_true(self):
        self.assertTrue(False is False)

    def test_raises(self):
        with self.assertRaises(NameError):
            self.dodo = gipsnich

