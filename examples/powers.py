#!/usr/bin/env python3

import jpylib as y

y.alert_level(y.L_TRACE)

data = [[ "exp " + str(exp) for exp in range(8)]]
for base in range(11):
    row = []
    for exp in range(8):
        row.append(base ** exp)
    data.append(row)


print(y.Table(data=data, align="lclr", have_header=True, corner=".").format())
