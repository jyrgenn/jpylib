#!/usr/bin/env python3

import jpylib as y

import os
import sys
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
        return json.loads(y.backquote("lib/read-secrets.py"))

    def setUp(self):
        os.makedirs(tmpdir, exist_ok=True)
        shutil.copyfile("lib/secrets", default_secrets)
        y.secrets.default_filename = default_secrets
        self.data = self.getdata() 

    def test_putsecret0(self):
        # should not trigger an error, wouldn't that be nice
        y.alert_level(4)
        key = "dumdi"
        secret = "schlummbaladumdibroing"
        with y.outputCaptured() as (out, err):
            y.putsecret(key, secret, options=["zip"])
            self.assertEqual(y.getsecret(key, error_exception=False), secret)
        self.assertEqual(os.stat(default_secrets).st_mode & 0o777, 0o600)

    def test_unknown_option_put(self):
        with self.assertRaises(y.secrets.OptionUnknownError):
            y.putsecret("foo", "bar", options=["zap"])

    def test_unknown_option_get(self):
        with y.outputCaptured() as (out, err):
            secret = y.getsecret("with-colon")
        self.assertEqual(out.getvalue(), "")
        compareto = """\
 invalid options in 'with-colon:...', maybe should be 'with-colon::...'"""
        # now pick the right output line (this is brittle, sorry, I know)
        msg = err.getvalue().split("\n")[1]
        self.assertEqual(msg.split(":", 2)[2], compareto)
        self.assertTrue(msg.startswith(default_secrets+":"))
        # again, another part of it
        msg = err.getvalue().split("\n")[0]
        self.assertEqual(msg.split(":", 2)[2],
                         " not a valid key:opts:value line")
        self.assertTrue(msg.startswith(default_secrets+":"))
        
    def test_getsecret(self):
        for key in self.data.keys():
            with y.outputCaptured() as (out, err):
                self.assertEqual(y.getsecret(key), self.data[key]["secret"])

    def test_getsecret_none(self):
        os.remove(default_secrets)
        with self.assertRaises(FileNotFoundError):
            for key in self.data.keys():
                self.assertEqual(y.getsecret(key), self.data[key]["secret"])
        

    def test_putall(self):
        for key in self.data.keys():
            with y.outputCaptured() as (out, err):
                y.putsecret(key, self.data[key]["secret"],
                            options=self.data[key]["opts"])
        newdata = self.getdata()
        self.assertEqual(self.data, newdata)

    def test_unknown_getsecret(self):
        with self.assertRaises(KeyError) as ctx:
            with y.outputCaptured():
                value = y.getsecret("ditt ham wer nich")
        self.assertEqual(ctx.exception.args,
                         ("cannot find secret for '{}' in '{}'",
                          'ditt ham wer nich', 'tmp/secrets'))
        with y.outputCaptured():
            value = y.getsecret("ditt ham wer nich", error_exception=False)
        self.assertIsNone(value)

    def test_tempfile(self):
        with self.assertRaises(FileExistsError) as ctx:
            tempfile = "tmp/.secrets.newtmp"
            open(tempfile, "w").close()
            y.putsecret("me", "and you")
        self.assertEqual(ctx.exception.args[0],
                         "temp file '{}' exists, aborting".format(tempfile))

    def test_main_run_noargs(self):
        out, err, status = y.backquote("jpylib/secrets.py", full_result=True)
        self.assertEqual(err, "usage: getsecret key [filename]\n")

    def test_main_run(self):
        key = "with-colon"
        out, err, status = y.backquote("jpylib/secrets.py {} {}"
                                       .format(key, default_secrets),
                                       full_result=True)
        self.assertEqual(out.rstrip(), self.data.get(key)["secret"])

    def test_main_call(self):
        key = "with-colon"
        with y.outputAndExitCaptured() as (out, err, status):
            sys.argv = ("getsecret", key, default_secrets)
            y.secrets.main()
        self.assertEqual(out.getvalue().rstrip(),
                         self.data.get(key)["secret"])

    def test_main_call_noargs(self):
        with y.outputAndExitCaptured() as (out, err, status):
            sys.argv = ("getsecret")
            y.secrets.main()
        self.assertEqual(status.value, "usage: getsecret key [filename]")

    def test_main_call_unfound(self):
        key = "p-convention"
        with y.outputAndExitCaptured() as (out, err, status):
            sys.argv = ("getsecret", key, default_secrets)
            y.secrets.main()
        self.assertEqual(out.getvalue(), "")
        self.assertEqual(status.value,
                         "getsecret: cannot find secret for '{}' in '{}'"
                         .format(key, default_secrets))
