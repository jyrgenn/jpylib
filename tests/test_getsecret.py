#!/usr/bin/env python3

import jpylib as y
from jpylib import *

import os
import json
import shutil
import unittest

# [x] single colon, just read
# [x] single colon, put and get
# [x] with skipping non-entry lines
# [x] double colon, no options, just read
# [x] double colon, no options, put & get
# [x] b64 option, get
# [x] b64 option, put
# [x] zip option, get
# [x] zip option, put
# [x] put existing one
# [x] put multiple existing ones
# [x] all still there
# [x] non-existent secrets file (with the main(), too)
# [ ] mode of file after putsecret
# [ ] not far too many putsecret comments in it

tmpdir = "tmp"
default_secrets = os.path.join(tmpdir, "secrets")

class SecretsTestcase(unittest.TestCase):

    def getdata(self):
        return json.loads(backquote("lib/split-secrets.py"))

    def setUp(self):
        os.makedirs(tmpdir, exist_ok=True)
        shutil.copyfile("lib/secrets", default_secrets)
        y.secrets.default_filename = default_secrets
        self.data = self.getdata() 

    def test_putsecret0(self):
        # should not trigger an error, wouldn't that be nice
        alert_level(4)
        key = "dumdi"
        secret = "schlummbaladumdibroing"
        y.putsecret(key, secret, options=["zip"])
        self.assertEqual(y.getsecret(key, error_exception=False), secret)
        self.assertEqual(os.stat(default_secrets).st_mode & 0o777, 0o600)

    def test_getsecret(self):
        for key in self.data.keys():
            self.assertEqual(y.getsecret(key), self.data[key]["secret"])

    def test_getsecret_none(self):
        os.remove(default_secrets)
        with self.assertRaises(FileNotFoundError):
            for key in self.data.keys():
                self.assertEqual(y.getsecret(key), self.data[key]["secret"])
        

    def test_putall(self):
        for key in self.data.keys():
            y.putsecret(key, self.data[key]["secret"],
                        options=self.data[key]["opts"])
        newdata = self.getdata()
        self.assertEqual(self.data, newdata)
