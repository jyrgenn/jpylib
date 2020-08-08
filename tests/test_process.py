#!/usr/bin/env python3

import jpylib as y
from jpylib import *

import unittest

class ProcessTestcase(unittest.TestCase):

    def setUp(self):
        pass

    def test_single_s(self):
        self.assertEqual(backquote("lib/doop"), "doop\n")

    def test_single_l(self):
        self.assertEqual(backquote(["lib/doop"]), "doop\n")

    def test_arg_s(self):
        self.assertEqual(backquote("echo dorp"), "dorp\n")
        
    def test_arg_l(self):
        self.assertEqual(backquote(["echo", "dopp"]), "dopp\n")
        
    def test_shell_false(self):
        self.assertEqual(backquote("echo dumi$_", shell=False), "dumi$_\n")
        
    def test_shell_true(self):
        self.assertEqual(backquote("echo domi$_", shell=True),
                         "domi/usr/bin/make\n")

    def test_no_shell_l(self):
        self.assertEqual(backquote(["echo", "dami$_"]), "dami$_\n")

    def test_shell_explicit(self):
        out = backquote("echo $shell", shell="/bin/tcsh")
        self.assertTrue(out, "/bin/tcsh\n")

    def test_shell_builtin(self):
        with self.assertRaises(FileNotFoundError):
            full_result = backquote("exit 13", full_result=True)
        full_result = backquote("exit 13", full_result=True, shell=True)
        self.assertEqual(full_result, ("", "", 13))


    def test_shell_meta(self):
        full_result = backquote("echo doodeedoo", full_result="plus")
        self.assertFalse(full_result[1])

        full_result = backquote("echo doodeedoo | cat", full_result="plus")
        self.assertTrue(full_result[1])

        full_result = backquote("'echo' doodeedoo", full_result="plus")
        self.assertTrue(full_result[1])
        
        full_result = backquote("echo doodeedoo", full_result="plus",
                                shell=True)
        self.assertTrue(full_result[1])
        
    def test_full(self):
        full_result = backquote("echo doodeedoo", full_result=True)
        self.assertEqual(full_result, ("doodeedoo\n", "", 0))

        full_result = backquote("echo doodeedoo", full_result=True, shell=True)
        self.assertEqual(full_result, ("doodeedoo\n", "", 0))

        full_result = backquote("echo doodeedoo 1>&2", full_result=True)
        self.assertEqual(full_result, ("", "doodeedoo\n", 0))

        full_result = backquote("echo doodeedoo; exit 13", full_result=True)
        self.assertEqual(full_result, ("doodeedoo\n", "", 13))

    def test_silent(self):

        full_result = backquote("echo doodeedoo", full_result=True)
        self.assertEqual(full_result, ("doodeedoo\n", "", 0))

        with self.assertRaises(ChildProcessError):
            backquote("echo doodeedoo 1>&2")
        backquote("echo doodeedoo 1>&2", silent=True)

        with self.assertRaises(ChildProcessError):
            backquote("echo doodeedoo; exit 13")
        backquote("echo doodeedoo; exit 13", silent=True)
