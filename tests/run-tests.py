#!/usr/bin/env python3

import unittest

testsuite = unittest.defaultTestLoader.discover("tests")
unittest.TextTestRunner().run(testsuite)

