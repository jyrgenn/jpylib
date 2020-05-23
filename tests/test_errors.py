#!/usr/bin/env python3

from pgetopt import parse
import unittest

# try to trigger all error conditions handled in the code (except the
# assertions, which have already been done)

argtest_descs = (
    # name,  optdesc,            min, max
    ("none", { "_arguments": () }, 0, 0,
     #(num, ok)*
     (0, True), (1, False), (2, False)),
    ("fix2", { "_arguments": ("source", "dest") }, 2, 2,
     (0, False), (1, False), (2, True), (3, False)),
    ("1or2", { "_arguments": ("source", "[dest]") }, 1, 2,
     (0, False), (1, True), (2, True), (3, False)),
    ("1plusa", { "_arguments": ("source", "...") }, 1, None,
     (0, False), (1, True), (2, True), (3, True)),
    ("1plusa", { "_arguments": ("source", "[dest...]") }, 1, None,
     (0, False), (1, True), (2, True), (3, True)),
    ("2plusa", { "_arguments": ("source", "dest...") }, 2, None,
     (0, False), (1, False), (2, True), (3, True), (4, True)),
    ("2plusb", { "_arguments": ("source", "dest", "...") }, 2, None,
     (0, False), (1, False), (2, True), (3, True), (4, True)),
    ("0plus",  { "_arguments": ("...") }, 2, None,
     (0, True), (1, True), (2, True), (3, True), (4, True)),
    ("dont", { "_arguments": "no arg counting done" }, None, None,
     (0, True), (1, True), (2, True), (3, True), (4, True)),
)

def mklist(len, el):
    result = []
    for i in range(len):
        result.append(el)
    return result

class ErrorTestCase(unittest.TestCase):

    def test_argCountSubs(self):
        """run all argtest_descs"""
        for atest in argtest_descs:
            name, optdesc, min, max, *cases = atest
            for num, ok in cases:
                with self.subTest(sub=f"{name}_{num}"):
                    argv = mklist(num, name)
                    if ok:
                        _, args = parse(optdesc, argv, exit_on_error=False)
                        self.assertEqual(args, argv)
                    else:
                        with self.assertRaises(IndexError):
                            parse(optdesc, argv, exit_on_error=False)


    def test_unknownOpt(self):
        """encounter unknown option"""
        with self.assertRaises(KeyError):
            parse({ "v": ("verbose", bool, 1, "increase verbosity") },
                  ["-d", "nunga"], exit_on_error=False)

    def test_falseArgument(self):
        """argument supplied to bool option"""
        with self.assertRaises(TypeError):
            parse({ "v": ("verbose", bool, 1, "increase verbosity") },
                  ["--verbose=19", "nunga"], exit_on_error=False)

    def test_missingArgument(self):
        """argument supplied to bool option"""
        with self.assertRaises(IndexError):
            parse({ "i": ("iterations", int, 1, "number of iterations") },
                  ["-i"], exit_on_error=False)
        with self.assertRaises(IndexError):
            parse({ "i": ("iterations", int, 1, "number of iterations") },
                  ["--iterations"], exit_on_error=False)
            
    def test_wrongArgument(self):
        """wrong option argument type"""
        with self.assertRaises(TypeError):
            parse({ "i": ("iterations", int, 1, "number of iterations") },
                  ["-i", "bunga"], exit_on_error=False)
        with self.assertRaises(TypeError):
            parse({ "i": ("iterations", int, 1, "number of iterations") },
                  ["--iterations", "bunga"], exit_on_error=False)

        
if __name__ == "__main__":
    unittest.main()

        
