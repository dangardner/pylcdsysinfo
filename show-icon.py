#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function
import sys
from pylcdsysinfo import LCDSysInfo

try:
    slot = int(sys.argv[1])
    if not 0 < slot <= 43:
        raise ValueError("Out of bounds")
except (ValueError, IndexError):
        print("Syntax: %s <1-43>" % (sys.argv[0]), file=sys.stderr)
        sys.exit(1)

d = LCDSysInfo()
d.display_icon(0, slot)
