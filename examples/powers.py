#!/usr/bin/env python3

import jpylib as y

y.alert_level(y.L_TRACE)

data = [[ "exp " + str(exp) for exp in range(8)]]
for base in range(11):
    row = []
    for exp in range(8):
        row.append(base ** exp)
    data.append(row)

data2 = [
    ["&", "A", "B"],
    ["1", "A1", "B1"],
    ["2", "A2", "B2"],

]


print(y.Table(data=data, corner="/\\\\/", cross="v*=@>+<^",
              vsep="=-", hsep=":|",
              align=["r*", "lclrl*"]).format())
print(y.Table(data=data2, corner=" ", cross="  -     ",
              vsep=["-", None], hsep=["|", None], border=None,
              align=["r*", "lclrl*"]).format())
print(y.Table(data=data2, corner=" ", cross="  -     ",
              vsep=[None, None], hsep=[" ", " "], border=None,
              cell_pad=[0, 0],
              align=["c*", None]).format())
