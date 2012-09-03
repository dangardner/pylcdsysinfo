#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
from pylcdsysinfo import LCDSysInfo, TextAlignment, TextColours

try:
    if int(sys.argv[1]) < 1 or int(sys.argv[1]) > 180:
        raise ValueError("Out of bounds")
except ValueError:
        print >>sys.stderr, "Syntax: %s <1-42>" % (sys.argv[0])
        sys.exit(1)

d = LCDSysInfo()
d.display_icon(0, int(sys.argv[1]))
