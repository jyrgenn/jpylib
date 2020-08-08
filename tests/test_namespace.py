#!/usr/bin/env python3

# much of the Namespace tests has already been done in the config tests

import jpylib as y

import unittest

ns_string = "Namespace(include='/etc/example/conf.d/*', site_name='w21', suffixes=['*.c', '*.h', '*.in'], nreps=15)"

class TemplateTestcase(unittest.TestCase):

    def setUp(self):
        self.ns = y.Namespace(
            include="/etc/example/conf.d/*",
            site_name="w21",
            suffixes=["*.c", "*.h", "*.in"],
            nreps=15,
        )
        pass

    def test_get(self):
        self.assertEqual(self.ns.get("site_name"), "w21")
        self.assertEqual(self.ns.site_name, "w21")

    def test_set1(self):
        self.ns.set("site_name", "w31")
        self.assertEqual(self.ns.site_name, "w31")

    def test_set2(self):
        self.ns.site_name = "w31"
        self.assertEqual(self.ns.site_name, "w31")

    def test_str(self):
        self.assertEqual(str(self.ns), ns_string)

    def test_repr(self):
        self.assertEqual(repr(self.ns), ns_string)


    def test_raises(self):
        with self.assertRaises(NameError):
            self.dodo = gipsnich

