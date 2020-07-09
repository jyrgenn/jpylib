#!/usr/bin/env python3
# Have all support function modules here at hand.

from .pgetopt import parse as pgetopts
from .print_level import L_ERROR, L_NOTICE, L_INFO, L_DEBUG, L_TRACE, \
    print_level_config, print_level, print_level_name, \
    print_level_up, print_level_zero, is_notice, is_info, is_debug, is_trace, \
    debug_vars, err, notice, info, debug, trace
from .fntrace import fntrace
from .stringreader import StringReader
from .kvs import parse_kvs
from .namespace import Namespace
from .config import Config
from .getsecret import getsecret

version = "$__package_version$"
