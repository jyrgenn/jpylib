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
#     print(end="", flush=True)

t_storethis = """
0000000
0 | | 0
0000000
0 | | 0
0000000
0 | | 0
0000000
"""

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
        table = y.format_table(data=self.data, template=t_template)
        self.assertEqual(table, """\
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
        table0 = y.table.Table(template=t_template, align="r*,n*")
        table = table0.format(data=self.data)
        self.assertEqual(table, """\
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
        table = y.format_table(data=self.data, template=t_template,
                               align="r*,lclrl*")
        self.assertEqual(table, """\
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
        table = y.format_table(self.data, template=t_template, align="lclr")
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
            result = y.format_table(data=self.data, align="lc*lr")

    def test_no_data(self):
        with self.assertRaises(AssertionError):
            result = y.table.Table(align="lclr*").format()

    def test_tformat0(self):
        self.assertEqual(y.format_table(data=data2, template=tformat0,
                                 align="cc*", cell_pad=None),
                         """\
  &   False True
-----------------
False False False
True  False True""")

    def test_tformat0a(self):
        self.assertEqual(y.format_table(data=data2, template=tformat0,
                                 align="cc*", cell_pad=[0]),
                         """\
  &   False True
-----------------
False False False
True  False True""")

    def test_tformat0b(self):
        table = y.format_table(data=data2, template=tformat0,
                        align="cc*", cell_pad=0)
        self.assertEqual(table, """\
  &   False True
-----------------
False False False
True  False True""")

    def test_tformat1(self):
        table = y.format_table(data=data2, template=tformat1, align="crr")
        self.assertEqual(table, """\
   &   | False   True
-------+--------------
 False | False  False
 True  | False   True""")

    def test_tformat2(self):
        table = y.format_table(data=data2, template=tformat2,
                               align="cll,")
        self.assertEqual(table,
                         r"""/-----------------------\
|   &   : False | True  |
|=======:===============|
| False : False | False |
|-------:---------------+
| True  : False | True  |
\-----------------------/""")

    def test_abc(self):
        table = y.format_table(data=data3, align="c*,",
                        template=t_abc)
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
        table = y.format_table(data=data3, align="c*,",
                        template=t_columns)
        self.assertEqual(table, """\
   *    |   10    |   100    |   1000
=========================================
      4 |      40 |      400 |      4000
     27 |     270 |     2700 |     27000
   3125 |   31250 |   312500 |   3125000
 823543 | 8235430 | 82354300 | 823543000""")

    def test_cell_pad_non_int_seq(self):
        with self.assertRaises(ValueError) as ectx:
            table = y.format_table(data=data3, align="c*,",
                            template=t_columns, cell_pad=["", ""])
        self.assertEqual(ectx.exception.args,
                         ("cell_pad is not a sequence of int, but ['', '']",))

    def test_cell_pad_too_long_seq(self):
        with self.assertRaises(ValueError) as ectx:
            table = y.format_table(data=data3, align="c*,",
                            template=t_columns, cell_pad=[1, 1, 1, 4])
        self.assertEqual(ectx.exception.args,
                         ("cell_pad is not a sequence len 1 or 2, but 4",))

    def test_cell_pad_wrong_type(self):
        with self.assertRaises(ValueError) as ectx:
            table = y.format_table(data=data3, align="c*,",
                            template=t_columns, cell_pad="")
        self.assertEqual(ectx.exception.args,
                         ("cell_pad is not None or int or seq of 2 ints: ''",))

    def test_align_wrong_type_in_seq(self):
        with self.assertRaises(ValueError) as ectx:
            table = y.format_table(data=data3, align=("c*", 3),
                            template=t_columns, cell_pad=None)
        self.assertEqual(ectx.exception.args,
                         ("align must be a string of one or two comma-separated fields, but is ('c*', 3)"
                          ,))

    def test_align_wrong_len_seq(self):
        with self.assertRaises(ValueError) as ectx:
            table = y.format_table(data=data3, align=[],
                            template=t_columns, cell_pad=None)
        self.assertEqual(ectx.exception.args,
                         ("align must be a string of one or two comma-separated fields, but is []"
                          ,))

    def test_align_wrong_type(self):
        with self.assertRaises(ValueError) as ectx:
            table = y.format_table(data=data3, align=3,
                            template=t_columns, cell_pad=None)
        self.assertEqual(ectx.exception.args,
                         ("align must be a string of one or two comma-separated fields, but is 3",))

    def test_template_line_too_long(self):
        with self.assertRaises(ValueError) as ectx:
            table = y.format_table(data=data3, align=3,
                            template=t_line_too_long, cell_pad=None)
        self.assertEqual(ectx.exception.args,
                         ("template line 4 must be 7 chars long, but is 8",))

    def test_template_too_few_lines(self):
        with self.assertRaises(ValueError) as ectx:
            table = y.format_table(data=data3, align=3,
                            template=t_too_few_lines, cell_pad=None)
        self.assertEqual(ectx.exception.args,
                         ("template must have 7 lines, not 6",))

    def test_columns_b(self):
        """Test fully blank template lines."""
        table = y.format_table(data=data3, align="c*,",
                        template=t_columns_b)
        self.assertEqual(table, """\

   *    |   10    |   100    |   1000
=========================================
      4 |      40 |      400 |      4000
     27 |     270 |     2700 |     27000
   3125 |   31250 |   312500 |   3125000
 823543 | 8235430 | 82354300 | 823543000""")

    def test_columns_c(self):
        """Test fully blank template lines."""
        table = y.format_table(data=data3, align="c*,",
                        template=t_columns_c)
        self.assertEqual(table, """\

   *    |   10    |   100    |   1000
=========================================
      4 |      40 |      400 |      4000
     27 |     270 |     2700 |     27000
   3125 |   31250 |   312500 |   3125000
 823543 | 8235430 | 82354300 | 823543000""")

    def test_columns_c_indent(self):
        """Test fully blank template lines."""
        table = y.format_table(data=data3, align="c*,",
                        template=t_columns_c, indent="huhu")
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
        table = y.format_table(data=data3, align="cr*,",
                        template=t_columns_d)
        self.assertEqual(table, """\
    *           10        100        1000

       4        40        400        4000
      27       270       2700       27000
    3125     31250     312500     3125000
  823543   8235430   82354300   823543000""")

    def test_template_box(self):
        """Test of template "box"."""
        table = y.format_table(data3, "box", align="cr*,")
        self.assertEqual(table, """\
╒════════╦═════════╤══════════╤═══════════╕
│   *    ║      10 │      100 │      1000 │
╞════════╬═════════╪══════════╪═══════════╡
│      4 ║      40 │      400 │      4000 │
├────────╫─────────┼──────────┼───────────┤
│     27 ║     270 │     2700 │     27000 │
├────────╫─────────┼──────────┼───────────┤
│   3125 ║   31250 │   312500 │   3125000 │
├────────╫─────────┼──────────┼───────────┤
│ 823543 ║ 8235430 │ 82354300 │ 823543000 │
╘════════╩═════════╧══════════╧═══════════╛""")
        
    def test_template_minimal(self):
        """Test of template "minimal"."""
        table = y.format_table(data3, "minimal", align="cr*,")
        self.assertEqual(table, """\
   *          10       100       1000
      4       40       400       4000
     27      270      2700      27000
   3125    31250    312500    3125000
 823543  8235430  82354300  823543000""")
        
    def test_template_columns(self):
        """Test of template "columns"."""
        table = y.format_table(data3, "columns", align="cr*,")
        self.assertEqual(table, """\
   *    |      10 |      100 |      1000
--------|---------|----------|-----------
      4 |      40 |      400 |      4000
     27 |     270 |     2700 |     27000
   3125 |   31250 |   312500 |   3125000
 823543 | 8235430 | 82354300 | 823543000""")
        
    def test_template_full(self):
        """Test of template "full"."""
        table = y.format_table(data3, "full", align="cr*,")
        self.assertEqual(table, """\
.-----------------------------------------.
|   *    |      10 |      100 |      1000 |
|=========================================|
|      4 |      40 |      400 |      4000 |
|--------+---------+----------+-----------|
|     27 |     270 |     2700 |     27000 |
|--------+---------+----------+-----------|
|   3125 |   31250 |   312500 |   3125000 |
|--------+---------+----------+-----------|
| 823543 | 8235430 | 82354300 | 823543000 |
.-----------------------------------------.""")
        
    def test_template_heads(self):
        """Test of template "heads"."""
        table = y.format_table(data3, "heads", align="cr*,")
        self.assertEqual(table, """\
   *           10        100        1000
-------- --------- ---------- -----------
      4        40        400        4000
     27       270       2700       27000
   3125     31250     312500     3125000
 823543   8235430   82354300   823543000""")
        
    def test_template_markdown(self):
        """Test of template "markdown"."""
        table = y.format_table(data3, "markdown", align="cr*,")
        self.assertEqual(table, """\
|   *    |      10 |      100 |      1000 |
|--------|---------|----------|-----------|
|      4 |      40 |      400 |      4000 |
|     27 |     270 |     2700 |     27000 |
|   3125 |   31250 |   312500 |   3125000 |
| 823543 | 8235430 | 82354300 | 823543000 |""")
        
    def test_template_stored(self):
        """Test of stored template."""
        y.table.store_template("stored 1", t_storethis)
        table = y.format_table(data3, "stored 1", align="cr*,")
        self.assertEqual(table, """\
   *    |      10 |      100 |      1000
      4 |      40 |      400 |      4000
     27 |     270 |     2700 |     27000
   3125 |   31250 |   312500 |   3125000
 823543 | 8235430 | 82354300 | 823543000""")
        self.assertTrue("stored 1" in y.table.template_names())
        y.table.remove_template("stored 1")

    def test_example_data(self):
        table = y.format_table(cell_pad=[0, 1])
        self.assertEqual(table, """\
(O:O) col 1   col 2   col 3
row 1 cell 12 cell 13 cell 14
row 2 cell 22 cell 23 cell 24
row 3 cell 32 cell 33 cell 34""")        
        
    def test_template_names(self):
        self.assertEqual(y.table.template_names(),
                         ["box", "columns", "full", "heads",
                          "markdown", "minimal"])

    def test_unknown_template(self):
        with self.assertRaises(KeyError) as ctx:
            table = y.format_table(template_name="dunno")
        self.assertEqual(ctx.exception.args[0],
                         "not a valid template name: 'dunno'")

    def test_store_existing_a(self):
        tname = "superduper"
        y.table.store_template(tname, t_storethis)
        with self.assertRaises(ValueError) as ctx:
            y.table.store_template(tname, t_storethis)
        self.assertEqual(ctx.exception.args[0],
                         "template {} already exists".format(repr(tname)))
        y.table.remove_template(tname)
        
    def test_store_existing_b(self):
        tname = "superduper"
        y.table.store_template(tname, t_storethis)
        y.table.store_template(tname, t_columns_d, replace=True)
        self.assertEqual(y.table.get_template(tname), t_columns_d)
        y.table.remove_template(tname)

        
    def test_remove_existing(self):
        tname = "superduper"
        y.table.store_template(tname, t_storethis)
        self.assertTrue(tname in y.table.template_names())
        y.table.remove_template(tname)
        self.assertFalse(tname in y.table.template_names())
        
    def test_remove_nonexisting_a(self):
        tname = "superduper"
        with self.assertRaises(KeyError) as ctx:
            y.table.remove_template(tname)
        self.assertEqual(ctx.exception.args[0],
                         "template {} does not exist".format(repr(tname)))

        
    def test_remove_nonexisting_b(self):
        tname = "superduper"
        # will simply not raise an Exception
        y.table.remove_template(tname, mustexist=False)
        
    def test_template_align_comma_a(self):
        """Test of stored template."""
        y.table.store_template("stored 1", t_storethis)
        table = y.format_table(data3, "stored 1", align="cr*,n")
        self.assertEqual(table, """\
   *    |      10 |      100 |      1000
      4 |      40 |      400 |      4000
     27 |     270 |     2700 |     27000
   3125 |   31250 |   312500 |   3125000
 823543 | 8235430 | 82354300 | 823543000""")
        self.assertTrue("stored 1" in y.table.template_names())
        y.table.remove_template("stored 1")

    def test_template_align_comma_b(self):
        """Test of stored template."""
        with self.assertRaises(ValueError) as context:
            table = y.format_table(data3, "minimal", align="cr*,n,c")
        self.assertEqual(str(context.exception),
                         "more than 2 comma-separated align strings: 'cr*,n,c'")
