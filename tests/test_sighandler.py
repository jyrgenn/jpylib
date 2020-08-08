# test the sanesighandler function decorator

import jpylib as y
import unittest

@y.sanesighandler
def func_keyboard_interrupt():
    print("right")
    y.err("aw rite!")
    raise KeyboardInterrupt()

@y.sanesighandler
def func_broken_pipe():
    print("std out")
    y.err("yeah shit!")
    raise BrokenPipeError()

class SighandlerTestcase(unittest.TestCase):

    def test_keyboard_interrupt(self):
        with y.outputAndExitCaptured() as (out, err, status):
            func_keyboard_interrupt()
        self.assertEqual(out.getvalue(), "right\n")
        #self.assertTrue(err.getvalue().endswith(" aw rite!\n"))
        self.assertEqual(status.value, 130)

    def test_broken_pipe(self):
        with y.outputAndExitCaptured() as (out, err, status):
            func_broken_pipe()
        self.assertEqual(out.getvalue(), "std out\n")
        #self.assertTrue(err.getvalue().endswith(" yeah shit!\n"))
        self.assertEqual(status.value, 141)
