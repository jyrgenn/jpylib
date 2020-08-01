#!/usr/bin/env python3

from jpylib import *
from jpylib.alerts import *
import unittest

# alerts tests

class AlertsTestcase(unittest.TestCase):
    
    def test_variables(self):
        """test module variable settings"""
        self.assertEqual(len(alert_levels), 5)
        self.assertEqual(len(alert_levels) - 1, alert_max_level)
        self.assertEqual(alert_level_level, L_NOTICE)
        self.assertEqual(alert_level_level, 1)
        self.assertEqual(alert_program, os.path.basename(sys.argv[0]))

    def test_config(self):
        alert_config(level=L_DEBUG, program="the_program",
                     syslog_facility=syslog.LOG_LPR)
        self.assertEqual(alert_level(), 3)
        self.assertEqual(get_mod_var("alert_program"), "the_program")
        self.assertEqual(get_mod_var("alert_syslog_facility"), syslog.LOG_LPR)

        self.assertTrue(not syslog_opened)
        nulldev = open("/dev/null", "w")
        alert_redirect(L_DEBUG, nulldev)
        alert_level(L_DEBUG)
        debug("should open syslog")
        alert_redirect(L_DEBUG, sys.stderr)
        nulldev.close()
        self.assertTrue(get_mod_var("syslog_opened"))

    def test_level_names(self):
        alert_level(L_DEBUG)
        self.assertEqual(alert_level_name(), "L_DEBUG")
        self.assertEqual(alert_level_name(0), "L_ERROR")
        self.assertEqual(alert_level_name(1), "L_NOTICE")
        self.assertEqual(alert_level_name(2), "L_INFO")
        self.assertEqual(alert_level_name(3), "L_DEBUG")
        self.assertEqual(alert_level_name(4), "L_TRACE")

        self.assertEqual(get_mod_var("L_ERROR"), 0)
        self.assertEqual(get_mod_var("L_NOTICE"), 1)
        self.assertEqual(get_mod_var("L_INFO"), 2)
        self.assertEqual(get_mod_var("L_DEBUG"), 3)
        self.assertEqual(get_mod_var("L_TRACE"), 4)

    def test_alert_level(self):
        alert_level("L_INFO")
        self.assertEqual(alert_level(), L_INFO)
        self.assertEqual(get_mod_var("alert_level_level"), L_INFO)
        alert_level(L_TRACE)
        self.assertEqual(alert_level(), L_TRACE)
        self.assertEqual(get_mod_var("alert_level_level"), L_TRACE)

    def test_redirect(self):
        alert_level(alert_max_level)
        msg = "Null Eins Zwei Drei Vier Fünf Sechs".split()

        with outputCaptured() as (out, err):
            for level in range(alert_max_level + 1):
                alert_redirect(level, sys.stderr)
                alert_if_level(level, msg[level])
        outs = out.getvalue()
        errs = err.getvalue()
        # ptty("err is", repr(errs))
        # ptty("out is", repr(outs))
        self.assertEqual(outs, "")
        lineno = 0
        for line in errs.split("\n"):
            if lineno <= alert_max_level:
                # ptty("line =", repr(line), "msg[lineno] =", repr(msg[lineno]))
                self.assertTrue(line.endswith(msg[lineno]))
            lineno += 1

        with outputCaptured() as (out, err):
            for level in range(alert_max_level + 1):
                alert_redirect(level, sys.stderr)
                alert_redirect(L_NOTICE, sys.stdout)
                alert_if_level(level, msg[level])
        lineno = 0
        outs = out.getvalue()
        errs = err.getvalue()
        # ptty("err is", repr(errs))
        # ptty("out is", repr(outs))
        self.assertTrue(outs.endswith("Eins\n"))
        for line in errs.split("\n"):
            if lineno == L_NOTICE:
                continue
            self.assertTrue(line.endswith(msg[lineno]))
            lineno += 1
            
