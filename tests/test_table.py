#!/usr/bin/env python3

import jpylib as y

import unittest

# stackoverflow.com/questions/5909873/how-can-i-pretty-print-ascii-tables-with-python
# has more examples

# def ptable(table, eol="<"):
#     print()
#     for line in table.split("\n"):
#         print(line, eol, sep="")
#     if not table.endswith("\n"):
#         print(">>>>>>> no newline")

t_template = r"""
.-----.
| | | |
|=====|
| | | |
|-+-+-|
| | | |
.-----.
"""

t_columns = """
0000000
0 | | 0
0=====0
0 | | 0
0000000
0 | | 0
0000000
"""

# blanks-only line
t_columns_b = """
       
0 | | 0
0=====0
0 | | 0
0000000
0 | | 0
0000000
"""

# line with guard character
t_columns_c = """
       ;
0 | | 0
0=====0
0 | | 0
0000000
0 | | 0
0000000
"""

# guard character in a slightly more plausible scenario
t_columns_d = """
0000000
       ;
       ;
       ;
0000000;
       ;
0000000
"""


# guard character in a slightly more plausible scenario
t_line_too_long = """
0000000
       ;
       ;
       ;
 0000000;
       ;
0000000
"""


# guard character in a slightly more plausible scenario
t_too_few_lines = """
0000000
       ;
       ;
0000000;
       ;
0000000
"""


t_abc = """
A-v-.-B
| : $ !
>=+=,=<
| : $ !
@-*-+-/
| : $ !
C_^_∆_D
"""

tformat0 = r"""
0000000
0     0
0-----0
0     0
0000000
0     0
0000000
"""

tformat1 = r"""
0000000
0 | 0 0
0-+-0-0
0 | 0 0
0000000
0 | 0 0
0000000
"""

tformat2 = r"""
/-----\
| : | |
|=:===|
| : | |
|-:---+
| : | |
\-----/
"""


data2 = [
    ["&", "False", "True"],
    ["False", "False", "False"],
    ["True", "False", "True"],

]


data3 = [
    ["*",           "10",      "100", "1000"],
    ["4",           "40",      "400", "4000"],
    ["27",         "270",     "2700",     "27000"],
    ["3125",     "31250",   "312500",   "3125000"],
    ["823543", "8235430", "82354300", "823543000"],
]


class TableTestcase(unittest.TestCase):

    def setUp(self):
        self.data = [[ "exp " + str(exp) for exp in range(8)]]
        for base in range(11):
            row = []
            for exp in range(8):
                row.append(base ** exp)
            self.data.append(row)

    def test_table_1(self):
        table = y.Table(data=self.data, template=t_template)
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
.---------------------------------------------------------------------.""")

    def test_table_2(self):
        table = y.Table(data=self.data, template=t_template,
                        align=["r*", None])
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
.---------------------------------------------------------------------.""")

    def test_table_3(self):
        table = y.Table(data=self.data, template=t_template,
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
.---------------------------------------------------------------------.""")

    def test_table_align(self):
        table = y.Table(template=t_template, align="lclr").format(
            data=self.data)
        self.assertEqual(table, """\
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
.---------------------------------------------------------------------.""")

    def test_invalid_align(self):
        with self.assertRaises(ValueError):
            result = y.Table(data=self.data, align="lc*lr").format()

    def test_no_data(self):
        with self.assertRaises(AssertionError):
            result = y.Table(align="lc*lr").format()

    def test_tformat0(self):
        self.assertEqual(y.Table(data=data2, template=tformat0,
                                 align="cc*", cell_pad=None).format(),
                         """\
  &   False True
-----------------
False False False
True  False True""")

    def test_tformat0a(self):
        self.assertEqual(y.Table(data=data2, template=tformat0,
                                 align="cc*", cell_pad=[0]).format(),
                         """\
  &   False True
-----------------
False False False
True  False True""")

    def test_tformat0b(self):
        table = y.Table(data=data2, template=tformat0,
                        align="cc*", cell_pad=0).format()
        self.assertEqual(table, """\
  &   False True
-----------------
False False False
True  False True""")

    def test_tformat1(self):
        table = y.Table(data=data2, template=tformat1, align=["crr"]).format()
        self.assertEqual(table, """\
   &   | False   True
-------+--------------
 False | False  False
 True  | False   True""")

    def test_tformat2(self):
        table = y.Table(data=data2, template=tformat2,
                        align=["cll", None]).format()
        self.assertEqual(table,
                         r"""/-----------------------\
|   &   : False | True  |
|=======:===============|
| False : False | False |
|-------:---------------+
| True  : False | True  |
\-----------------------/""")

    def test_abc(self):
        table = y.Table(data=data3, align=["c*", None],
                        template=t_abc).format()
        self.assertEqual(table, """\
A--------v---------.----------.-----------B
|   *    :   10    $   100    $   1000    !
>========+=========,==========,===========<
|      4 :      40 $      400 $      4000 !
@--------*---------+----------+-----------/
|     27 :     270 $     2700 $     27000 !
@--------*---------+----------+-----------/
|   3125 :   31250 $   312500 $   3125000 !
@--------*---------+----------+-----------/
| 823543 : 8235430 $ 82354300 $ 823543000 !
C________^_________∆__________∆___________D""")

    def test_columns(self):
        table = y.Table(data=data3, align=["c*", None],
                        template=t_columns).format()
        self.assertEqual(table, """\
   *    |   10    |   100    |   1000
=========================================
      4 |      40 |      400 |      4000
     27 |     270 |     2700 |     27000
   3125 |   31250 |   312500 |   3125000
 823543 | 8235430 | 82354300 | 823543000""")

    def test_cell_pad_non_int_seq(self):
        with self.assertRaises(ValueError) as ectx:
            table = y.Table(data=data3, align=["c*", None],
                            template=t_columns, cell_pad=["", ""])
        self.assertEqual(ectx.exception.args,
                         ("cell_pad is not a sequence of int, but ['', '']",))

    def test_cell_pad_too_long_seq(self):
        with self.assertRaises(ValueError) as ectx:
            table = y.Table(data=data3, align=["c*", None],
                            template=t_columns, cell_pad=[1, 1, 1, 4])
        self.assertEqual(ectx.exception.args,
                         ("cell_pad is not a sequence len 1 or 2, but 4",))

    def test_cell_pad_wrong_type(self):
        with self.assertRaises(ValueError) as ectx:
            table = y.Table(data=data3, align=["c*", None],
                            template=t_columns, cell_pad="")
        self.assertEqual(ectx.exception.args,
                         ("cell_pad is not None or int or seq of 2 ints: ''",))

    def test_align_wrong_type_in_seq(self):
        with self.assertRaises(ValueError) as ectx:
            table = y.Table(data=data3, align=("c*", 3),
                            template=t_columns, cell_pad=None)
        self.assertEqual(ectx.exception.args,
                         ("align is not a sequence of str|None, but ('c*', 3)"
                          ,))

    def test_align_wrong_len_seq(self):
        with self.assertRaises(ValueError) as ectx:
            table = y.Table(data=data3, align=[],
                            template=t_columns, cell_pad=None)
        self.assertEqual(ectx.exception.args,
                         ("align must be sequence of len 1 or 2, not 0"
                          ,))

    def test_align_wrong_type(self):
        with self.assertRaises(ValueError) as ectx:
            table = y.Table(data=data3, align=3,
                            template=t_columns, cell_pad=None)
        self.assertEqual(ectx.exception.args,
                         ("align must be str or None or a seq of str|None, "
                             + "but is 3",))

    def test_template_line_too_long(self):
        with self.assertRaises(ValueError) as ectx:
            table = y.Table(data=data3, align=3,
                            template=t_line_too_long, cell_pad=None)
        self.assertEqual(ectx.exception.args,
                         ("template line is not 7 chars: 8 (line 4)",))

    def test_template_too_few_lines(self):
        with self.assertRaises(ValueError) as ectx:
            table = y.Table(data=data3, align=3,
                            template=t_too_few_lines, cell_pad=None)
        self.assertEqual(ectx.exception.args,
                         ("template must have 7 lines, not 6",))

    def test_columns_b(self):
        """Test fully blank template lines."""
        table = y.Table(data=data3, align=["c*", None],
                        template=t_columns_b).format()
        self.assertEqual(table, """\

   *    |   10    |   100    |   1000
=========================================
      4 |      40 |      400 |      4000
     27 |     270 |     2700 |     27000
   3125 |   31250 |   312500 |   3125000
 823543 | 8235430 | 82354300 | 823543000""")

    def test_columns_c(self):
        """Test fully blank template lines."""
        table = y.Table(data=data3, align=["c*", None],
                        template=t_columns_c).format()
        self.assertEqual(table, """\

   *    |   10    |   100    |   1000
=========================================
      4 |      40 |      400 |      4000
     27 |     270 |     2700 |     27000
   3125 |   31250 |   312500 |   3125000
 823543 | 8235430 | 82354300 | 823543000""")

    def test_columns_c_indent(self):
        """Test fully blank template lines."""
        table = y.Table(data=data3, align=["c*", None],
                        template=t_columns_c, indent="huhu").format()
        self.assertEqual(table, """\
huhu
huhu   *    |   10    |   100    |   1000
huhu=========================================
huhu      4 |      40 |      400 |      4000
huhu     27 |     270 |     2700 |     27000
huhu   3125 |   31250 |   312500 |   3125000
huhu 823543 | 8235430 | 82354300 | 823543000""")

    def test_columns_d(self):
        """Test fully blank template lines."""
        table = y.Table(data=data3, align=["cr*", None],
                        template=t_columns_d).format()
        self.assertEqual(table, """\
    *           10        100        1000

       4        40        400        4000
      27       270       2700       27000
    3125     31250     312500     3125000
  823543   8235430   82354300   823543000""")

