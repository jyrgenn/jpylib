#!/usr/bin/env python3
# multiplication table as in issue #23

import jpylib as y

data = [["*", 1, 2, 3],
        [1, 1, 2, 3],
        [2, 2, 4, 6],
        [3, 3, 6, 9]]

template = """
0000000
0 | 0 0
0-+-0-0
0 | 0 0
0000000
0 | 0 0
0000000"""

print(y.Table(data=data, template=template).format())
