#!/usr/bin/env python3
# print the table templates with examples

import jpylib as y

for name in y.table.template_names():
    print()
    example = y.format_table(template_name=name, align="c*,")
    print("{}\n{}\n\n{}".format(name, len(name) * "-", example))
print()
