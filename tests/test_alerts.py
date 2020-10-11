#!/usr/bin/env python3

from jpylib import *
from jpylib.alerts import *
import unittest

# alerts tests

class AlertsTestcase(unittest.TestCase):

    def setUp(self):
        alert_init()
    
    def test_variables(self):
        """test module variable settings"""
        self.assertEqual(len(alert_levels), 5)
        self.assertEqual(len(alert_levels) - 1, alcf().max_level)
        self.assertEqual(alcf().level, L_NOTICE)
        self.assertEqual(alcf().level, 1)
        self.assertEqual(alcf().program, os.path.basename(sys.argv[0]))

    def test_config(self):
        alert_config(level=L_DEBUG, program="the_program",
                     syslog_facility=syslog.LOG_LPR)
        self.assertEqual(alert_level(), 3)
        self.assertEqual(alcf().program, "the_program")
        self.assertEqual(alcf().syslog_facility, syslog.LOG_LPR)

        debug("Step on it, Arnold! Step on it!") # need to trigger syslog open
        self.assertTrue(alcf().syslog_opened)
        nulldev = open("/dev/null", "w")
        alert_redirect(L_DEBUG, nulldev)
        alert_level(L_DEBUG)
        alert_redirect(L_DEBUG, sys.stderr)
        nulldev.close()
        self.assertTrue(alcf().syslog_opened)

    def test_level_names(self):
        alert_level(L_DEBUG)
        self.assertEqual(alert_level_name(), "L_DEBUG")
        self.assertEqual(alert_level_name(0), "L_ERROR")
        self.assertEqual(alert_level_name(1), "L_NOTICE")
        self.assertEqual(alert_level_name(2), "L_INFO")
        self.assertEqual(alert_level_name(3), "L_DEBUG")
        self.assertEqual(alert_level_name(4), "L_TRACE")

        self.assertEqual(L_ERROR, 0)
        self.assertEqual(L_NOTICE, 1)
        self.assertEqual(L_INFO, 2)
        self.assertEqual(L_DEBUG, 3)
        self.assertEqual(L_TRACE, 4)

    def test_alert_level(self):
        l = alert_level("L_INFO")
        self.assertEqual(alert_level(), L_INFO)
        self.assertEqual(alcf().level, L_INFO)
        alert_level(L_TRACE)
        self.assertEqual(alert_level(), L_TRACE)
        self.assertEqual(alcf().level, L_TRACE)
        alert_level_up()
        self.assertEqual(alert_level(), L_TRACE)
        alert_level_zero()
        self.assertEqual(alert_level(), L_ERROR)
        alert_level_up()
        self.assertEqual(alert_level(), L_NOTICE)
        
        alert_level_zero()
        self.assertEqual([is_notice(), is_info(), is_debug(), is_trace()],
                         [False, False, False, False])
        alert_level_up()
        self.assertEqual([is_notice(), is_info(), is_debug(), is_trace()],
                         [True, False, False, False])
        alert_level_up()
        self.assertEqual([is_notice(), is_info(), is_debug(), is_trace()],
                         [True, True, False, False])
        alert_level_up()
        self.assertEqual([is_notice(), is_info(), is_debug(), is_trace()],
                         [True, True, True, False])
        alert_level_up()
        self.assertEqual([is_notice(), is_info(), is_debug(), is_trace()],
                         [True, True, True, True])
        alert_level_up()
        self.assertEqual([is_notice(), is_info(), is_debug(), is_trace()],
                         [True, True, True, True])

        alert_level_zero()
        with outputCaptured() as (out, err):
            notice("check check check 2")
        self.assertEqual(err.getvalue(), "")
        
        alert_level_up()
        with outputCaptured() as (out, err):
            notice("check check check 4")
        self.assertEqual(err.getvalue(), "check check check 4\n")

    def test_lambda_arg(self):
        with outputCaptured() as (out, err):
            notice("this is", lambda: "a test")
        self.assertEqual(err.getvalue(), "this is a test\n")

    def test_num_level(self):
        with outputCaptured() as (out, err):
            alert_redirect(1, 1)
            notice("this is", lambda: "a test")
        self.assertEqual(out.getvalue(), "this is a test\n")

    def test_debug_vars(self):
        a = 3
        b = "this is a test"
        c = a * b
        with outputCaptured() as (out, err):
            alert_redirect(L_DEBUG, sys.stderr)
            alert_level(L_DEBUG)
            debug_vars("a", "b", "c")
        self.assertEqual(err.getvalue(), """DBG VAR a: 3
DBG VAR b: 'this is a test'
DBG VAR c: 'this is a testthis is a testthis is a test'\n""")

    def test_error(self):
        alert_level(L_TRACE)
        self.assertEqual(alcf().had_errors, False)
        with outputCaptured() as (out, err):
            error("an error")
        self.assertTrue(err.getvalue().endswith("an error\n"))
        self.assertEqual(alcf().had_errors, True)

    def test_fatal(self):
        with outputAndExitCaptured() as (out, err, status):
            fatal("too bad!")
        self.assertTrue(err.getvalue().endswith(" too bad!\n"))
        self.assertEqual(status.value, 1)
        with outputAndExitCaptured() as (out, err, status):
            fatal("oy vey!", exit_status=13)
        self.assertTrue(err.getvalue().endswith(" oy vey!\n"))
        self.assertEqual(status.value, 13)
        

    def test_notice(self):
        alert_level(L_TRACE)
        with outputCaptured() as (out, err):
            notice("las noticias")
        self.assertTrue(err.getvalue().endswith("las noticias\n"))

    def test_info(self):
        alert_level(L_TRACE)
        with outputCaptured() as (out, err):
            info("terminal")
        self.assertTrue(err.getvalue().endswith("terminal\n"))

    def test_info_timestamp_0(self):
        alert_level(L_TRACE)
        alert_config(timestamps=True)
        with outputCaptured() as (out, err):
            info("terminal")
        value = err.getvalue()
        self.assertTrue(value.endswith("terminal\n"))
        self.assertTrue(value.startswith(y.isotime()))

    def test_debug(self):
        alert_init(level=L_TRACE)
        with outputCaptured() as (out, err):
            debug("adbsdbgdb")
        #ptty(f"ERRVALUE({alert_level()})", err.getvalue())
        self.assertTrue(err.getvalue().endswith("adbsdbgdb\n"))

    def test_trace(self):
        alert_level(L_TRACE)
        with outputCaptured() as (out, err):
            trace("lines")
        self.assertTrue(err.getvalue().endswith("lines\n"))

    def test_tracef(self):
        alert_level(L_TRACE)
        template = "foo {:3} bar {} dong"
        args = 13, "nuggi"
        shouldbe = template.format(*args)
        with outputCaptured() as (out, err):
            tracef(template, *args)
        self.assertTrue(err.getvalue().strip().endswith(shouldbe))

    def test_debugf(self):
        alert_level(L_DEBUG)
        template = "foo {:3} bar {} dong"
        args = 13, "nuggi"
        shouldbe = template.format(*args)
        with outputCaptured() as (out, err):
            debugf(template, *args)
        self.assertTrue(err.getvalue().strip().endswith(shouldbe))

    def test_infof(self):
        alert_level(L_INFO)
        template = "foo {:3} bar {} dong"
        args = 13, "nuggi"
        shouldbe = template.format(*args)
        with outputCaptured() as (out, err):
            infof(template, *args)
        self.assertTrue(err.getvalue().strip().endswith(shouldbe))

    def test_noticef(self):
        alert_level(L_NOTICE)
        template = "foo {:3} bar {} dong"
        args = 13, "nuggi"
        shouldbe = template.format(*args)
        with outputCaptured() as (out, err):
            noticef(template, *args)
        self.assertTrue(err.getvalue().strip().endswith(shouldbe))

    def test_errorf(self):
        alert_level(L_ERROR)
        template = "foo {:3} bar {} dong"
        args = 13, "nuggi"
        shouldbe = template.format(*args)
        with outputCaptured() as (out, err):
            errorf(template, *args)
        self.assertTrue(err.getvalue().strip().endswith(shouldbe))

    def test_fatalf(self):
        alert_level(L_ERROR)
        template = "foo {:3} bar {} dong"
        args = 13, "nuggi"
        shouldbe = template.format(*args)
        with outputAndExitCaptured() as (out, err, status):
            fatalf(template, *args)
        value = err.getvalue().strip()
        #print("\n{}\n{}".format(shouldbe, value))
        self.assertTrue(value.endswith(shouldbe))
        self.assertEqual(status.value, 1)

    def test_redirect(self):
        alert_level(alcf().max_level)
        msg = "Null Eins Zwei Drei Vier Fünf Sechs".split()

        with outputCaptured() as (out, err):
            for level in range(alcf().max_level + 1):
                alert_redirect(level, sys.stderr)
                alert_if_level(level, msg[level])
        outs = out.getvalue()
        errs = err.getvalue()
        # ptty("err is", repr(errs))
        # ptty("out is", repr(outs))
        self.assertEqual(outs, "")
        lineno = 0
        for line in errs.split("\n"):
            if lineno <= alcf().max_level:
                # ptty("line =", repr(line), "msg[lineno] =", repr(msg[lineno]))
                self.assertTrue(line.endswith(msg[lineno]))
            lineno += 1

        with outputCaptured() as (out, err):
            for level in range(alcf().max_level + 1):
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
            
    def test_temp_alert_level(self):
        the_level = 2
        temp_level = 3
        y.alert_level(the_level)
        self.assertEqual(y.alert_level(), the_level)
        try:
            with temporary_alert_level(temp_level):
                self.assertEqual(y.alert_level(), temp_level)
                raise NotImplementedError()
        except NotImplementedError:
            pass
        self.assertEqual(y.alert_level(), the_level)
            
