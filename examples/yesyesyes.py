#!/usr/bin/env python3
# a yes(1) in python

import sys
import jpylib as y

@y.sanesighandler
def main():
    while True:
        print(*(sys.argv[1:] or ["y"]))

main()
