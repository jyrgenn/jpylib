#!/usr/bin/env python3

import jpylib as y
from jpylib import *

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

default_secrets = "tmp/secrets"

class SecretsTestcase(unittest.TestCase):

    def setUp(self):
        shutil.copyfile("lib/secrets", default_secrets)
        y.secrets.default_filename = default_secrets

    def test_putsecret(self):
        # should not trigger an error, wouldn't that be nice
        alert_level(4)
        y.putsecret("dumdi", "schlummbaladumdibroing", options=["zip"])
        self.assertEqual(y.getsecret("dumdi"), "schlummbaladumdibroing")
