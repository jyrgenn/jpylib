#!/usr/bin/env python3

# tests for the Multiset class

import jpylib as y

import unittest

ms_string = "jpylib.multiset.Multiset((4, 5, 6, 6))"

class MultisetTestcase(unittest.TestCase):

    def setUp(self):
        self.ms = y.Multiset([4, 5, 6, 6])
        pass

    def test_str(self):
        self.assertEqual(str(self.ms), ms_string)

    def test_add(self):
        self.ms.add(7)
        self.ms.add(7)
        self.assertEqual(str(self.ms),
                         "jpylib.multiset.Multiset((4, 5, 6, 6, 7, 7))")

    def test_count(self):
        self.assertEqual(self.ms.count(6), 2)
        self.assertEqual(self.ms.count(113), 0)

    def test_set_count(self):
        self.ms.set_count(6, 3)
        self.assertEqual(str(self.ms),
                         "jpylib.multiset.Multiset((4, 5, 6, 6, 6))")
        self.ms.set_count(6, 0)
        self.assertEqual(str(self.ms),
                         "jpylib.multiset.Multiset((4, 5))")

    def test_remove(self):
        self.ms.remove(6)
        self.assertEqual(str(self.ms),
                         "jpylib.multiset.Multiset((4, 5, 6))")
        self.ms.remove(6)
        self.assertEqual(str(self.ms),
                         "jpylib.multiset.Multiset((4, 5))")
        self.ms.remove(6)
        self.assertEqual(str(self.ms),
                         "jpylib.multiset.Multiset((4, 5))")
        
    def test_remove_all(self):
        self.ms.remove(6, True)
        self.assertEqual(str(self.ms),
                         "jpylib.multiset.Multiset((4, 5))")
        self.ms.remove(6, True)
        self.assertEqual(str(self.ms),
                         "jpylib.multiset.Multiset((4, 5))")

    def test_len(self):
        self.assertEqual(len(self.ms), 4)
        self.ms.add("foofoo")
        self.assertEqual(len(self.ms), 5)
        self.ms.add("foofoo")
        self.assertEqual(len(self.ms), 6)
        

    def test_repr(self):
        self.assertEqual(str(self.ms), repr(self.ms))
