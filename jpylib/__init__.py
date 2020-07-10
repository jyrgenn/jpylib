#!/usr/bin/env python3
# Have all support function modules here at hand.

from .pgetopt import parse as pgetopts
from .alerts import L_ERROR, L_NOTICE, L_INFO, L_DEBUG, L_TRACE, \
    alert_config, alert_level, alert_level_name, \
    alert_level_up, alert_level_zero, is_notice, is_info, is_debug, is_trace, \
    debug_vars, fatal, err, notice, info, debug, trace
from .fntrace import fntrace
from .stringreader import StringReader
from .kvs import parse_kvs
from .namespace import Namespace
from .config import Config
from .getsecret import getsecret
from .getsecret import main as getsecret_main
from .sighandler import sanesighandler

version = "$__package_version$"
