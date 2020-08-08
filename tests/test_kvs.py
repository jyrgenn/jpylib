#!/usr/bin/env python3

import jpylib as y

import unittest

class KVSTestcase(unittest.TestCase):

    def setUp(self):
        pass

    def test_empty(self):
        result = y.parse_kvs("")
        self.assertEqual(result, {})

    def test_one_pair(self):
        result = y.parse_kvs("a=b")
        self.assertEqual(result, dict(a="b"))

    def test_one_pair_empty_list(self):
        result = y.parse_kvs("a=[]")
        self.assertEqual(result, dict(a=[]))

    def test_three_pairs(self):
        result = y.parse_kvs("a=b,c=d,g=98056")
        self.assertEqual(result, dict(a="b", c="d", g="98056"))

    def test_three_pairs_int(self):
        result = y.parse_kvs("a=b,c=d,g=98056", intvals=True)
        self.assertEqual(result, dict(a="b", c="d", g=98056))

    def test_list1(self):
        result = y.parse_kvs("a=[b,c,d]", intvals=True)
        self.assertEqual(result, dict(a=["b","c","d"]))


    def test_kvs_1(self):
        self.assertEqual(y.parse_kvs("signals=[1,2,15],action=terminate",
                                     intvals=True),
                         dict(signals=[1,2,15], action="terminate"))

    def test_kvs_2(self):
        self.assertEqual(y.parse_kvs("cfg={file=~/etc/foo.conf,syntax=INI}"),
                         dict(cfg=dict(file="~/etc/foo.conf", syntax="INI")))

    def test_kvs_1(self):
        self.assertEqual(y.parse_kvs("foo=bar,dang=[1,2,15],d={a=b,c=[d,e,f]}",
                                     intvals=True),
                         dict(foo="bar",
                              dang=[1,2,15],
                              d=dict(a="b", c=["d","e","f"])))

    def test_syntax_error_1(self):
        with self.assertRaises(y.kvs.SyntaxError):
            print(y.parse_kvs("foo=bar,dang=[1,,2,15]],d={a=b,c=[d,e,f]}"))

    def test_syntax_error_2(self):
        with self.assertRaises(y.kvs.SyntaxError):
            print(y.parse_kvs("foo=bar,dang=[1,,2,15,d={a=b,c=[d,e,f]}"))

    def test_syntax_error_3(self):
        with self.assertRaises(y.kvs.SyntaxError):
            print(y.parse_kvs("foo=bar,dang=[1,,2,15}"))

    def test_nested_list1(self):
        value = y.parse_kvs("dang=[1,,2,[]]", intvals=True)
        self.assertEqual(value, dict(dang=[1, "", 2, []]))

    def test_nested_list2(self):
        value = y.parse_kvs("dang=[1,2,[]]", intvals=True)
        self.assertEqual(value, dict(dang=[1, 2, []]))

