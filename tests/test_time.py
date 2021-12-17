#!/usr/bin/env python3

import jpylib as y

import time
import datetime
import unittest

class TimeTestcase(unittest.TestCase):

    def setUp(self):
        self.now = datetime.datetime(2020, 8, 30, 11, 25, 48, 567108)

    def test_isotime(self):
        # Take care to call isotime() roughly at the start of a second, so
        # date(1) will not show a different second.
        time.sleep((1000000 - datetime.datetime.now().microsecond) / 1000000.0)
        self.assertEqual(y.isotime(),
                         y.backquote("date +%Y%m%d:%H%M%S").strip())

    def test_isotime_ms(self):
        self.assertEqual(y.isotime_ms(self.now), "20200830:112548.567")

    def test_iso_time(self):
        self.assertEqual(y.iso_time(self.now), "2020-08-30T11:25:48")

    def test_iso_time_(self):
        self.assertEqual(y.iso_time(self.now, sep="_"), "2020-08-30_11:25:48")

    def test_iso_time_us(self):
        self.assertEqual(y.iso_time_us(self.now), "2020-08-30T11:25:48.567108")

    def test_iso_time_ms(self):
        self.assertEqual(y.iso_time_ms(self.now), "2020-08-30T11:25:48.567")


