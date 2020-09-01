#!/usr/bin/env python3

import jpylib as y

y.alert_level(y.L_TRACE)

data = [[""] + [ "exp " + str(exp) for exp in range(8)]]
for base in range(10):
    row = ["base " + str(base)]
    for exp in range(8):
        row.append(base ** exp)
    data.append(row)

data2 = [
    ["&", "False", "True"],
    ["False", "False", "False"],
    ["True", "False", "True"],

]

t_template = r"""
.-----.
| | | |
|=====|
| | | |
|-|-+-|
| | | |
.-----.
"""

print(y.Table(data=data, align=["c*", None], template=t_template).format())

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

t_0 = """
0000000
0000000
0000000
0000000
0000000
0000000
0000000
"""


print(y.Table(data=data2, template=tformat1,
              align=["cll"]).format())
print(y.Table(data=data2, template=tformat2,
              align=["cll", None]).format())
print(y.Table(data=data2, template=tformat0,
              align="c*", cell_pad=None).format())
print(y.Table(data=data2, template=t_0,
              align="c*", cell_pad=[0, 1]).format())
