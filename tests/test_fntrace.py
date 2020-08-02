#!/usr/bin/env python3

from jpylib import *

import unittest


class FNTraceTestcase(unittest.TestCase):

    def test_fntrace(self):
        alert_level(L_DEBUG)
        with outputCaptured() as (out, err):
            @tracefn
            def callee(k, l, m):
                return k * l * m
            b = callee(2, 3, 5)
            self.assertEqual(b, 30)
        self.assertEqual(err.getvalue(), "")
        alert_level(L_TRACE)
        with outputCaptured() as (out, err):
            @tracefn
            def callee(k, l, m):
                return k * l * m
            b = callee(7, 11, 13)
            self.assertEqual(b, 1001)
        self.assertEqual(err.getvalue(), "TRC call callee(7, 11, 13)\n")
        with outputCaptured() as (out, err):
            @tracefn
            def nothing(*args, **kwargs):
                pass
            nothing(4, "/usr/bin/", 19, {3+4}, smoke="mirrors", cloak="dagger")
        self.assertEqual(err.getvalue(),
                         "TRC call nothing(4, '/usr/bin/', 19, {7},"
                         " smoke='mirrors', cloak='dagger')\n")
