#!/usr/bin/env python3
# multiplication table as in issue #23

import copy
import jpylib as y

datadim = 11

data = [["*", *range(datadim)]]

for i in range(datadim):
    data.append([i, *range(datadim)])
    for j in range(datadim):
        i_ = i + 1
        j_ = j + 1
        data[i_][j_] = i * j
#        print(f"data[{i_}][{j_}] = {data[i_][j_]}")

# for i in range(datadim):
#     print(i, ":", data[i])

template = """
0000000
0 | 0 0
0-+-0-0
0 | 0 0
0000000
0 | 0 0
0000000"""

print(y.table.Table(data=data, align=["rn*", None], template=template).format())
