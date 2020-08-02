#!/usr/bin/env python3

from jpylib import *

import os
import re
import sys
import unittest
import subprocess

cfg = None

class ConfigTestcase(unittest.TestCase):

    def setUp(self):
        global cfg
        cfg = Config(
            include="/etc/example/conf.d/*",
            site_name="w21",
            suffixes=["*.c", "*.h", "*.in"],
            nreps=15,
        )

    def test_update(self):
        cfg.update({"site_name": "w21.org", "suffixes":["*.py", "*.pl"]})
        self.assertEqual(cfg.__dict__, {
            "include": "/etc/example/conf.d/*",
            "site_name": "w21.org",
            "suffixes":["*.py", "*.pl"],
            "nreps": 15,
        })
        with self.assertRaises(KeyError):
            cfg.update({"domain": "w21.org", "suffixes":["*.gz", "*.z"]})
        cfg.update({"domain": "w21.org", "_tmp_var": "c00l", "_haxz": 1337},
                   reject_unknown=False)
        self.assertEqual(cfg.__dict__, {
            "domain": "w21.org",
            "include": "/etc/example/conf.d/*",
            "site_name": "w21.org",
            "suffixes":["*.py", "*.pl"],
            "nreps": 15,
        })
        
    def test_set_and_get(self):
        self.assertEqual(cfg.get("nreps"), 15)
        self.assertEqual(cfg.get("include"), "/etc/example/conf.d/*")
        with self.assertRaises(KeyError):
            cfg.set("domain", "w21.org")
        cfg.set("domain", "w21.org", reject_unknown=False)
        self.assertEqual(cfg.get("domain"), "w21.org")
        with self.assertRaises(KeyError):
            cfg.get("owner")

    def test_load(self):
        cfg = Config()
        cfg2 = Config(
            pi=3.14,
            csource='foomla.c',
            adasource='foomla.ada',
            includes=[
                '/etc/foomla/config',
                '/etc/foomla/conf.d/*'
            ],
        )
        with self.assertRaises(KeyError):
            cfg.load_from("lib/testconfig.conf")
        cfg.load_from("lib/testconfig.conf", reject_unknown=False)
        self.assertEqual(cfg.__dict__, cfg2.__dict__)

