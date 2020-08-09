#!/usr/bin/env python3

import jpylib as y

import unittest

readme = "doc/pgetopt.md"

class ReadmeTestcase(unittest.TestCase):

    def setUp(self):
        pass

    def test_ToC(self):
        """Check if the generated table of contents is present.

        This is not a check for completeness, and it must be changed once the
        subheading used here is changed.

        """
        am_motivated = False
        with open(readme) as f:
            for line in f:
                if "[Motivation](#motivation)" in line:
                    am_motivated = True
        self.assertTrue(am_motivated)

    def test_errtable(self):
        """Check if the generated error table is present and complete."""
        source = "jpylib/pgetopt.py"
        errors = y.backquote("sed -n '/^Error/s/ .*//p' " + source)
        errorset = set(errors.split())
        with open(readme) as f:
            for line in f:
                if line.startswith("| Error"):
                    the_error = line.split()[1]
                    # will raise KeyError if the_error is not in the errorset
                    errorset.remove(the_error)
        self.assertEqual(errorset, set())

