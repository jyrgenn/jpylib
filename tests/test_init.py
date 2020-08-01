#!/usr/bin/env python3

from jpylib import *

import os
import re
import sys
import unittest
import subprocess

# assorted tests

# the version may be a generated version number or the unexpanded token if
# tested outside of a package (which is the only way to do it, right?)
version_re = r"^(20\d\d\.\d\d\d\d?.\d\d\d\d?|\$__package_version\$)$"


class InitTestcase(unittest.TestCase):

    def test_ttys(self):
        tty_in = ttyi()
        self.assertEqual(tty_in.__class__.__name__, "TextIOWrapper")
        tty_in2 = ttyi()
        self.assertIs(tty_in, tty_in2)
        self.assertEqual(tty_in.name, "/dev/tty")
        ttyi(close=True)

        tty_out = ttyo()
        self.assertEqual(tty_out.__class__.__name__, "TextIOWrapper")
        tty_out2 = ttyo()
        self.assertIs(tty_out, tty_out2)
        self.assertEqual(tty_out.name, "/dev/tty")
        ttyo(close=True)
        
    def test_vars(self):
        self.assertTrue(re.match(version_re, version))
        self.assertEqual(program, sys.argv[0].split("/")[-1])
        
        proc = subprocess.Popen(["sh", "-c", "echo $HOME"],
                                stdout=subprocess.PIPE)
        proc.wait()
        result = str(proc.stdout.read(), "utf-8").strip()
        proc.stdout.close()
        self.assertEqual(real_home, result)
        self.assertEqual(real_home, home)


