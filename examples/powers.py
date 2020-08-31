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

tformat1 = r"""
/-----\
| : | |
|=:===|
| : | |
|-:---+
| : | |
\-----/
"""



tformat2 = r"""
0000000
0 | 0 0
0-+-0-0
0 | 0 0
0000000
0 | 0 0
0000000
"""

tformat0 = r"""
0000000
0 0 0 0
0000000
0 0 0 0
0000000
0 0 0 0
0000000
"""


print(y.Table(data=data2, template=tformat1,
              align=["r*", "lclrl*"]).format())
print(y.Table(data=data2, template=tformat2,
              align=["r*", "lclrl*"]).format())
print(y.Table(data=data2, template=tformat0,
              align=["c*", None]).format())
