#!/usr/bin/env python3

from jpylib import pgetopts
import unittest


# test replacing the default usage message

class UsageTestcase(unittest.TestCase):

    def test_usage0(self):
        """-h/--hounds option"""
        ovc, args = pgetopts({
            "v": ("verbose", bool, 1, "increase verbosity"),
            "z": ("zounds", int, 1, "number of zounds"),
            "_arguments": [],
        }, ["-v"], exit_on_error=False)
        self.assertEqual(ovc.ovc_usage_msg(),
                         "usage: {} [-vz]".format(ovc._program))

    def test_usage1(self):
        """-h/--hounds option"""
        ovc, args = pgetopts({
            "v": ("verbose", bool, 1, "increase verbosity"),
            "z": ("zounds", int, 1, "number of zounds"),
            "_arguments": ["mangia"],
        }, ["-v", "foo!"], exit_on_error=False)
        self.assertEqual(ovc.ovc_usage_msg(),
                         "usage: {} [-vz] mangia".format(ovc._program))

    def test_usage2(self):
        """-h/--hounds option"""
        ovc, args = pgetopts({
            "v": ("verbose", bool, 1, "increase verbosity"),
            "z": ("zounds", int, 1, "number of zounds"),
            "_arguments": ["mangia", "[file1 ...]"],
        }, ["-v", "foo!"], exit_on_error=False)
        self.assertEqual(ovc.ovc_usage_msg(),
                         "usage: {} [-vz] mangia [file1 ...]".format(
                             ovc._program))

    def test_usage_own(self):
        """-h/--hounds option"""
        ovc, args = pgetopts({
            "v": ("verbose", bool, 1, "increase verbosity"),
            "z": ("zounds", int, 1, "number of zounds"),
            "_arguments": ["mangia", "[file1 ...]"],
            "_usage": "usage: gniddle [-v] [-z 5] mangia [file1 ...]"
        }, ["-v", "foo!"], exit_on_error=False)
        self.assertEqual(
            ovc.ovc_usage_msg(),
            "usage: gniddle [-v] [-z 5] mangia [file1 ...]")

    def test_usage_program(self):
        """-h/--hounds option"""
        ovc, args = pgetopts({
            "v": ("verbose", bool, 1, "increase verbosity"),
            "z": ("zounds", int, 1, "number of zounds"),
            "_arguments": ["mangia", "[file1 ...]"],
            "_program": "schnörkelate",
        }, ["-v", "foo!"], exit_on_error=False)
        self.assertEqual(ovc.ovc_usage_msg(),
                         "usage: schnörkelate [-vz] mangia [file1 ...]")


    def test_usage_string_arguments(self):
        """_arguments as string"""
        ovc, args = pgetopts({
            "v": ("verbose", bool, 0, "increase verbosity"),
            "_arguments": "...",
            "_program": "lala",
        })
        self.assertEqual(ovc.ovc_usage_msg(), "usage: lala [-v] ...")


    def test_usage_empty_string_arguments(self):
        """_arguments as string"""
        ovc, args = pgetopts({
            "v": ("verbose", bool, 0, "increase verbosity"),
            "_arguments": "",
            "_program": "lala",
        })
        self.assertEqual(ovc.ovc_usage_msg(), "usage: lala [-v]")

    def test_usage_empty_list_arguments(self):
        """_arguments as string"""
        ovc, args = pgetopts({
            "v": ("verbose", bool, 0, "increase verbosity"),
            "_arguments": [],
            "_program": "lala",
        }, [])
        self.assertEqual(ovc.ovc_usage_msg(), "usage: lala [-v]")
