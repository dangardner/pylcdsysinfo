#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
from pylcdsysinfo import LCDSysInfo

try:
    slot = int(sys.argv[1])
    if not 0 < slot <= 43:
        raise ValueError("Out of bounds")
except ValueError:
        print >>sys.stderr, "Syntax: %s <1-43>" % (sys.argv[0])
        sys.exit(1)

d = LCDSysInfo()
d.display_icon(0, slot)
