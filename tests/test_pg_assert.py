#!/usr/bin/env python3

from jpylib import pgetopts
import unittest

# tests about triggering assertion errors
class AssertionsTestcase(unittest.TestCase):

    def test_okOptType(self):
        """valid option types"""
        for typ in bool, str, int, all:
            with self.subTest(i=typ):
                pgetopts({
                    "s": ("schmooze", typ, 0, "schmooziness"),
                }, [])

    def test_invOptType(self):
        """invalid option types"""
        for typ in float, "dudi", 3:
            with self.subTest(i=typ):
                with self.assertRaises(AssertionError):
                    pgetopts({
                        "s": ("schmooze", typ, 0, "schmooziness"),
                    }, [])

    def test_shortDesc(self):
        """short option descriptor"""
        with self.assertRaises(AssertionError):
            pgetopts({
                "s": ("schmooze", bool, 0),
            }, [])

    def test_longDesc(self):
        """long option descriptor"""
        with self.assertRaises(AssertionError):
            pgetopts({
                "s": ("schmooze", bool, 0, "huhu", "huhu", "huhu"),
            }, [])

    def test_DescType(self):
        """invalid descriptor type"""
        with self.assertRaises(AssertionError):
            pgetopts({
                "s": 17,
            }, [])

    def test_NameType(self):
        """invalid option name type"""
        with self.assertRaises(AssertionError):
            pgetopts({
                "s": (12, bool, 0, "increase schmooziness"),
            }, [])

    def test_Long_Key(self):
        """option key too long"""
        with self.assertRaises(AssertionError):
            pgetopts({
                "sc": ("schmooze", bool, 0, "increase schmooziness"),
            }, [])

    def test_Invalid_Keyword(self):
        """invalid keyword"""
        with self.assertRaises(AssertionError):
            pgetopts({
                "s": ("schmooze", bool, 0, "increase schmooziness"),
                "__arguments": ["file1", "...", "destination"],
            }, ["bla", "blubb"])

    def test_Valid_Keyword(self):
        """valid keyword"""
        given_args = ["bla", "blubb"]
        ovc, args = pgetopts({
            "s": ("schmooze", bool, 0, "increase schmooziness"),
            "_arguments": ["file1", "...", "destination"],
        }, given_args)
        self.assertEqual(args, given_args)

        
