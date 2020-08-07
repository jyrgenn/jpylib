#!/usr/bin/env python3

import jpylib as y
from jpylib import *

import os
import json
import shutil
import unittest

# [x] single colon, just read
# [ ] single colon, put and get
# [x] with skipping non-entry lines
# [x] double colon, no options, just read
# [ ] double colon, no options, put & get
# [x] b64 option, get
# [ ] b64 option, put
# [x] zip option, get
# [ ] zip option, put
# [ ] put existing one
# [ ] put multiple existing ones
# [ ] all still there
# [ ] non-existent secrets file (with the main(), too)
# [ ] mode of file after putsecret
# [ ] not far too many putsecret comments in it

tmpdir = "tmp"
default_secrets = os.path.join(tmpdir, "secrets")

class SecretsTestcase(unittest.TestCase):

    def getdata(self):
        return json.loads(backquote("lib/split-secrets.py", touchy=True)[0])

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
        self.assertEqual(y.getsecret(key), secret)

    def test_getsecret(self):
        for key in self.data.keys():
            self.assertEqual(y.getsecret(key), self.data[key]["secret"])

    def test_putall(self):
        for key in self.data.keys():
            y.putsecret(key, self.data[key]["secret"], self.data[key]["opts"])
        newdata = self.getdata()
        self.assertEqual(self.data, newdata)
