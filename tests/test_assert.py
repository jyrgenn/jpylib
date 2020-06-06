#!/usr/bin/env python3

from pgetopt import parse
import unittest

# tests about triggering assertion errors
class AssertionsTestcase(unittest.TestCase):

    def test_okOptType(self):
        """valid option types"""
        for typ in bool, str, int, None:
            with self.subTest(i=typ):
                parse({
                    "s": ("schmooze", typ, 0, "schmooziness"),
                }, [])

    def test_invOptType(self):
        """invalid option types"""
        for typ in float, "dudi", 3:
            with self.subTest(i=typ):
                with self.assertRaises(AssertionError):
                    parse({
                        "s": ("schmooze", typ, 0, "schmooziness"),
                    }, [])

    def test_shortDesc(self):
        """short option descriptor"""
        with self.assertRaises(AssertionError):
            parse({
                "s": ("schmooze", bool, 0),
            }, [])

    def test_longDesc(self):
        """long option descriptor"""
        with self.assertRaises(AssertionError):
            parse({
                "s": ("schmooze", bool, 0, "huhu", "huhu", "huhu"),
            }, [])

    def test_DescType(self):
        """invalid descriptor type"""
        with self.assertRaises(AssertionError):
            parse({
                "s": 17,
            }, [])

    def test_NameType(self):
        """invalid option name type"""
        with self.assertRaises(AssertionError):
            parse({
                "s": (12, bool, 0, "increase schmooziness"),
            }, [])

    def test_Long_Key(self):
        """option key too long"""
        with self.assertRaises(AssertionError):
            parse({
                "sc": ("schmooze", bool, 0, "increase schmooziness"),
            }, [])

    def test_Invalid_Keyword(self):
        """invalid keyword"""
        with self.assertRaises(AssertionError):
            parse({
                "s": ("schmooze", bool, 0, "increase schmooziness"),
                "__arguments": ["file1", "...", "destination"],
            }, ["bla", "blubb"])

    def test_Valid_Keyword(self):
        """valid keyword"""
        given_args = ["bla", "blubb"]
        ovc, args = parse({
            "s": ("schmooze", bool, 0, "increase schmooziness"),
            "_arguments": ["file1", "...", "destination"],
        }, given_args)
        self.assertEqual(args, given_args)



if __name__ == "__main__":
    unittest.main()

        
