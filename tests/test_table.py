#!/usr/bin/env python3

import jpylib as y

import unittest

# stackoverflow.com/questions/5909873/how-can-i-pretty-print-ascii-tables-with-python
# has more examples

class TableTestcase(unittest.TestCase):

    def setUp(self):
        self.data = [[ "exp " + str(exp) for exp in range(8)]]
        for base in range(11):
            row = []
            for exp in range(8):
                row.append(base ** exp)
            self.data.append(row)

    def test_table_1(self):
        table = y.Table(data=self.data, have_header=True, corner=".")
        self.assertEqual(table.format(),
                         """\
.---------------------------------------------------------------------.
| exp 0 | exp 1 | exp 2 | exp 3 | exp 4 | exp 5  | exp 6   | exp 7    |
|=====================================================================|
|     1 |     0 |     0 |     0 |     0 |      0 |       0 |        0 |
|-------+-------+-------+-------+-------+--------+---------+----------|
|     1 |     1 |     1 |     1 |     1 |      1 |       1 |        1 |
|-------+-------+-------+-------+-------+--------+---------+----------|
|     1 |     2 |     4 |     8 |    16 |     32 |      64 |      128 |
|-------+-------+-------+-------+-------+--------+---------+----------|
|     1 |     3 |     9 |    27 |    81 |    243 |     729 |     2187 |
|-------+-------+-------+-------+-------+--------+---------+----------|
|     1 |     4 |    16 |    64 |   256 |   1024 |    4096 |    16384 |
|-------+-------+-------+-------+-------+--------+---------+----------|
|     1 |     5 |    25 |   125 |   625 |   3125 |   15625 |    78125 |
|-------+-------+-------+-------+-------+--------+---------+----------|
|     1 |     6 |    36 |   216 |  1296 |   7776 |   46656 |   279936 |
|-------+-------+-------+-------+-------+--------+---------+----------|
|     1 |     7 |    49 |   343 |  2401 |  16807 |  117649 |   823543 |
|-------+-------+-------+-------+-------+--------+---------+----------|
|     1 |     8 |    64 |   512 |  4096 |  32768 |  262144 |  2097152 |
|-------+-------+-------+-------+-------+--------+---------+----------|
|     1 |     9 |    81 |   729 |  6561 |  59049 |  531441 |  4782969 |
|-------+-------+-------+-------+-------+--------+---------+----------|
|     1 |    10 |   100 |  1000 | 10000 | 100000 | 1000000 | 10000000 |
.---------------------------------------------------------------------.
""")

    def test_table_2(self):
        table = y.Table(data=self.data, have_header=True, corner=".",
                        align=["r", None])
        self.assertEqual(table.format(),
                         """\
.---------------------------------------------------------------------.
| exp 0 | exp 1 | exp 2 | exp 3 | exp 4 |  exp 5 |   exp 6 |    exp 7 |
|=====================================================================|
|     1 |     0 |     0 |     0 |     0 |      0 |       0 |        0 |
|-------+-------+-------+-------+-------+--------+---------+----------|
|     1 |     1 |     1 |     1 |     1 |      1 |       1 |        1 |
|-------+-------+-------+-------+-------+--------+---------+----------|
|     1 |     2 |     4 |     8 |    16 |     32 |      64 |      128 |
|-------+-------+-------+-------+-------+--------+---------+----------|
|     1 |     3 |     9 |    27 |    81 |    243 |     729 |     2187 |
|-------+-------+-------+-------+-------+--------+---------+----------|
|     1 |     4 |    16 |    64 |   256 |   1024 |    4096 |    16384 |
|-------+-------+-------+-------+-------+--------+---------+----------|
|     1 |     5 |    25 |   125 |   625 |   3125 |   15625 |    78125 |
|-------+-------+-------+-------+-------+--------+---------+----------|
|     1 |     6 |    36 |   216 |  1296 |   7776 |   46656 |   279936 |
|-------+-------+-------+-------+-------+--------+---------+----------|
|     1 |     7 |    49 |   343 |  2401 |  16807 |  117649 |   823543 |
|-------+-------+-------+-------+-------+--------+---------+----------|
|     1 |     8 |    64 |   512 |  4096 |  32768 |  262144 |  2097152 |
|-------+-------+-------+-------+-------+--------+---------+----------|
|     1 |     9 |    81 |   729 |  6561 |  59049 |  531441 |  4782969 |
|-------+-------+-------+-------+-------+--------+---------+----------|
|     1 |    10 |   100 |  1000 | 10000 | 100000 | 1000000 | 10000000 |
.---------------------------------------------------------------------.
""")

    def test_table_2(self):
        table = y.Table(data=self.data, have_header=True, corner=".",
                        align=["r*", "lclrl*"])
        self.assertEqual(table.format(),
                         """\
.---------------------------------------------------------------------.
| exp 0 | exp 1 | exp 2 | exp 3 | exp 4 |  exp 5 |   exp 6 |    exp 7 |
|=====================================================================|
| 1     |   0   | 0     |     0 | 0     | 0      | 0       | 0        |
|-------+-------+-------+-------+-------+--------+---------+----------|
| 1     |   1   | 1     |     1 | 1     | 1      | 1       | 1        |
|-------+-------+-------+-------+-------+--------+---------+----------|
| 1     |   2   | 4     |     8 | 16    | 32     | 64      | 128      |
|-------+-------+-------+-------+-------+--------+---------+----------|
| 1     |   3   | 9     |    27 | 81    | 243    | 729     | 2187     |
|-------+-------+-------+-------+-------+--------+---------+----------|
| 1     |   4   | 16    |    64 | 256   | 1024   | 4096    | 16384    |
|-------+-------+-------+-------+-------+--------+---------+----------|
| 1     |   5   | 25    |   125 | 625   | 3125   | 15625   | 78125    |
|-------+-------+-------+-------+-------+--------+---------+----------|
| 1     |   6   | 36    |   216 | 1296  | 7776   | 46656   | 279936   |
|-------+-------+-------+-------+-------+--------+---------+----------|
| 1     |   7   | 49    |   343 | 2401  | 16807  | 117649  | 823543   |
|-------+-------+-------+-------+-------+--------+---------+----------|
| 1     |   8   | 64    |   512 | 4096  | 32768  | 262144  | 2097152  |
|-------+-------+-------+-------+-------+--------+---------+----------|
| 1     |   9   | 81    |   729 | 6561  | 59049  | 531441  | 4782969  |
|-------+-------+-------+-------+-------+--------+---------+----------|
| 1     |  10   | 100   |  1000 | 10000 | 100000 | 1000000 | 10000000 |
.---------------------------------------------------------------------.
""")

    def test_table_align(self):
        table = y.Table(corner=".", align="lclr")
        self.assertEqual(table.format(data=self.data, have_header=True),
                         """\
.---------------------------------------------------------------------.
| exp 0 | exp 1 | exp 2 | exp 3 | exp 4 | exp 5  | exp 6   | exp 7    |
|=====================================================================|
| 1     |   0   | 0     |     0 |     0 |      0 |       0 |        0 |
|-------+-------+-------+-------+-------+--------+---------+----------|
| 1     |   1   | 1     |     1 |     1 |      1 |       1 |        1 |
|-------+-------+-------+-------+-------+--------+---------+----------|
| 1     |   2   | 4     |     8 |    16 |     32 |      64 |      128 |
|-------+-------+-------+-------+-------+--------+---------+----------|
| 1     |   3   | 9     |    27 |    81 |    243 |     729 |     2187 |
|-------+-------+-------+-------+-------+--------+---------+----------|
| 1     |   4   | 16    |    64 |   256 |   1024 |    4096 |    16384 |
|-------+-------+-------+-------+-------+--------+---------+----------|
| 1     |   5   | 25    |   125 |   625 |   3125 |   15625 |    78125 |
|-------+-------+-------+-------+-------+--------+---------+----------|
| 1     |   6   | 36    |   216 |  1296 |   7776 |   46656 |   279936 |
|-------+-------+-------+-------+-------+--------+---------+----------|
| 1     |   7   | 49    |   343 |  2401 |  16807 |  117649 |   823543 |
|-------+-------+-------+-------+-------+--------+---------+----------|
| 1     |   8   | 64    |   512 |  4096 |  32768 |  262144 |  2097152 |
|-------+-------+-------+-------+-------+--------+---------+----------|
| 1     |   9   | 81    |   729 |  6561 |  59049 |  531441 |  4782969 |
|-------+-------+-------+-------+-------+--------+---------+----------|
| 1     |  10   | 100   |  1000 | 10000 | 100000 | 1000000 | 10000000 |
.---------------------------------------------------------------------.
""")

    def test_true(self):
        self.assertTrue(False is False)

    def test_invalid_align(self):
        with self.assertRaises(ValueError):
            result = y.Table(data=self.data, have_header=True, corner=".",
                             align="lc*lr").format()

    def test_no_data(self):
        with self.assertRaises(AssertionError):
            result = y.Table(have_header=True, corner=".",
                             align="lc*lr").format()

