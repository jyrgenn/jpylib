#!/usr/bin/env python3

# much of the Namespace tests has already been done in the config tests

import jpylib as y

import unittest

ns_string = "Namespace(include='/etc/example/conf.d/*', site_name='w21', suffixes=['*.c', '*.h', '*.in'], nreps=15)"

class NamespaceTestcase(unittest.TestCase):

    def setUp(self):
        self.ns = y.Namespace(
            include="/etc/example/conf.d/*",
            site_name="w21",
            suffixes=["*.c", "*.h", "*.in"],
            nreps=15,
        )
        pass

    def test_update(self):
        self.ns.update(dict(site_name="w31", _bully=[], nreps=13),
                       reject_unknown=True, skip_underscore=True)
        self.assertEqual(str(self.ns),
                         str(y.Namespace(include="/etc/example/conf.d/*",
                                              site_name="w31",
                                              suffixes=["*.c", "*.h", "*.in"],
                                              nreps=13,)))

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

    def test_reread(self):
        self.assertEqual(str(self.ns), str(eval("y."+repr(self.ns))))

    def test_setitem_known(self):
        self.ns.nreps = 15
        self.assertEqual(self.ns.nreps, 15)
        self.ns["nreps"] = 17
        self.assertEqual(self.ns.nreps, 17)

    def test_setitem_new(self):
        key = "huhu"
        self.assertEqual(self.ns.get(key), None)
        self.ns[key] = "I'm here"
        self.assertEqual(self.ns.huhu, "I'm here")

    def test_getitem_unknown(self):
        self.assertEqual(self.ns.get("aERbkRMYVBkzhOnSt"), None)

    def test_getitem_known(self):
        self.assertEqual(self.ns["include"], "/etc/example/conf.d/*")

    def test_delitem(self):
        key = "huhu"
        self.ns.set(key, "I'm here")
        self.assertEqual(self.ns.huhu, "I'm here")
        del self.ns[key]
        self.assertEqual(self.ns.get(key), None)

    def test_iter(self):
        the_keys = set(self.ns.__dict__.keys())
        found = set()
        for key in self.ns:
            found.add(key)
        self.assertEqual(the_keys, found)

    def test_contains(self):
        self.assertEqual(bool("include" in self.ns), True)
        self.assertEqual(bool("rXBlD3DtB9zEPRz3d" in self.ns), False)

    def test_len(self):
        self.assertEqual(len(self.ns.__dict__), len(self.ns))
