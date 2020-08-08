#!/usr/bin/env python3

from jpylib.pgetopt import *
import unittest

# assorted tests from the docs

schmooze_descs = {
    "s": ("schmooze", bool, 0, "increase schmooziness"),
    "o": ("output_file", str, None, "output file (or stdout)", "NAME"),
    "n": ("repetitions", int, 3, "number of repetitions"),
    "d": ("debug", str, [], "debug topics", "DEBUG_TOPIC"),
    "_arguments": ["string_to_print", "..."],
    "_help_header": "print a string a number of times",
    "_help_footer": "This is just an example program.",
}

blark_descs = {
    "v": ("verbose", bool, False, "be verbose"),
    "o": ("output_file", str, "/dev/stdout", "output file", "PATHNAME"),
    "i": ("iterations", int, 1, "number of iterations"),
    "_arguments": ["gnumm", "..."],
}

class BlarkTestcase(unittest.TestCase):

    # blark -v -o /tmp/blark.out -i 3 gnuddle fuddle -a ruddle
    def test_fromREADME(self):
        """blark example from the README"""
        argv = "-v -o /tmp/blark.out -i 3 gnuddle fuddle -a ruddle".split(" ")
        ovc, args = parse(blark_descs, argv, exit_on_error=False)
        self.assertEqual(ovc.ovc_values(),
                         dict(verbose=1, output_file="/tmp/blark.out",
                              iterations=3))
        self.assertEqual(args, "gnuddle fuddle -a ruddle".split(" "))
    

class SchmoozeTestcase(unittest.TestCase):

    def test_noArgs(self):
        """no arguments (needs 1)"""
        with self.assertRaises(OptionError) as cm:
            parse(schmooze_descs, [], exit_on_error=False)
        self.assertEqual(cm.exception.args, (ErrorMinarg, 1))

    def test_OneArg(self):
        """one argument, no options"""
        ovc, args = parse(schmooze_descs, ["huhu"], exit_on_error=False)
        self.assertEqual(ovc.ovc_values(),
                         dict(schmooze=0, output_file=None,
                              repetitions=3, debug=[]))
        self.assertEqual(args, ["huhu"])

    def test_fiveArgs(self):
        """5 args"""
        ovc, args = parse(schmooze_descs,
                          ["huhu", "haha", "dada", "dodo", "bu"],
                          exit_on_error=False)
        self.assertEqual(ovc.ovc_values(),
                         dict(schmooze=0, output_file=None,
                              repetitions=3, debug=[]))
        self.assertEqual(args, ["huhu", "haha", "dada", "dodo", "bu"])


    def test_oneArg_ss(self):
        """1 arg -ss"""
        ovc, args = parse(schmooze_descs,
                          ["-ss", "huhu"],
                          exit_on_error=False)
        self.assertEqual(ovc.ovc_values(),
                         dict(schmooze=2, output_file=None,
                              repetitions=3, debug=[]))
        self.assertEqual(args, ["huhu"])


    def test_wrongOpt(self):
        """wrong opt"""
        with self.assertRaises(OptionError) as cm:
            ovc, args = parse(schmooze_descs,
                              ["-d", "print", "--output_file=hamburg",
                               "haha", "dada"],
                              exit_on_error=False)
        self.assertEqual(cm.exception.args, (ErrorNotopt, "output_file"))

    def test_moreOpts(self):
        """more opts"""
        ovc, args = parse(schmooze_descs,
                          ["-d", "print", "--output-file=hamburg",
                           "haha", "dada"],
                          exit_on_error=False)
        self.assertEqual(ovc.ovc_values(),
                         dict(schmooze=0, output_file="hamburg",
                              repetitions=3, debug=["print"]))
        self.assertEqual(args, ["haha", "dada"])

    def test_noOpts_dashdash(self):
        """no opts"""
        ovc, args = parse(schmooze_descs,
                          ["--", "-d", "print", "--output_file=hamburg",
                           "haha", "dada"],
                          exit_on_error=False)
        self.assertEqual(ovc.ovc_values(),
                         dict(schmooze=0, output_file=None,
                              repetitions=3, debug=[]))
        self.assertEqual(args,
                         ["-d", "print", "--output_file=hamburg",
                          "haha", "dada"])

        
