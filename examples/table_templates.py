#!/usr/bin/env python3
# print the table templates with examples

import jpylib as y

for name in y.table.template_names():
    print()
    example = y.table.get_template_example(name, align=["c*", None])
    print("{}\n{}\n\n{}".format(name, len(name) * "-", example))
print()
