#!/usr/bin/env python3

import jpylib as y
from jpylib import *

import os
import json
import shutil
import unittest

# [ ] single colon, just read
# [ ] single colon, put and get
# [ ] with skipping non-entry lines
# [ ] double colon, no options, just read
# [ ] double colon, no options, put & get
# [ ] b64 option, put & get
# [ ] zip option, put & get
# [ ] put existing one
# [ ] put multiple existing ones
# [ ] all still there
# [ ] non-existent secrets file (with the main(), too)
# [ ] mode of file after putsecret
# [ ] not far too many putsecret comments in it

tmpdir = "tmp"
default_secrets = os.path.join(tmpdir, "secrets")

class SecretsTestcase(unittest.TestCase):

    def setUp(self):
        os.makedirs(tmpdir, exist_ok=True)
        shutil.copyfile("lib/secrets", default_secrets)
        y.secrets.default_filename = default_secrets
        self.data = \
            json.loads(backquote("lib/split-secrets.py", touchy=True)[0])

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

    
