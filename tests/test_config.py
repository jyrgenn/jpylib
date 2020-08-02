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

    def test_load_files(self):
        cfg = Config(
            pi=3.14,
            csource='foomla.c',
            adasource='foomla.ada',
            includes=[
                '/etc/foomla/config',
                '/etc/foomla/conf.d/*'
            ],
        )
        with outputCaptured() as (out, err):
            nloaded = cfg.load_config_files([
                "lib/testconfig2.conf",
                "lib/testconfig3.conf",
                "lib/testconfig4.conf",     # does not exist
            ], notice_func=notice)
        self.assertEqual(cfg.__dict__, Config(
            pi=3.1415,
            csource='foomla.c',
            adasource='foomla.ada',
            includes=[
                '/usr/local/etc/foomla/config',
                '/usr/local/etc/foomla/conf.d/*'
            ],
        ).__dict__)
        self.assertEqual(nloaded, 2)
        self.assertEqual(err.getvalue(), """\
configuration loaded from lib/testconfig2.conf
configuration loaded from lib/testconfig3.conf
""")
        with self.assertRaises(OSError) as context:
            nloaded = cfg.load_config_files([
                "lib/testconfig2.conf",
                "lib/testconfig3.conf",
                "lib/testconfig4.conf",     # does not exist
            ], files_must_exist=True)
        self.assertEqual(type(context.exception), FileNotFoundError)
        with self.assertRaises(SyntaxError) as context:
            cfg.load_from("lib/testconfig5.conf")
        self.assertIn("Error in config file", str(context.exception))


    def test_from_string(self):
        cfg = Config()
        cfg.update_from_string(
            "foo=bar,dang=[1,2,15],d={a=b,c=[d,e,f],quux=blech},e=not",
            reject_unknown=False,
        )
        cfg2 = Config(
            foo="bar",
            dang=[1, 2, 15],
            d={
                "a": "b",
                "c": ["d", "e", "f"],
                "quux": "blech",
            },
            e="not"
        )
        self.assertEqual(cfg.__dict__, cfg2.__dict__)
