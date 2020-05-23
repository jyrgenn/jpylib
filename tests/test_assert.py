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



if __name__ == "__main__":
    unittest.main()

        
