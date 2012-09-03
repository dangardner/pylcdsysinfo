#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
from pylcdsysinfo import LCDSysInfo, TextAlignment, TextColours

try:
    if int(sys.argv[1]) < 0 or int(sys.argv[1]) > 7:
        raise ValueError("Out of bounds")
except ValueError:
        print >>sys.stderr, "Syntax: %s <0-7>" % (sys.argv[0])
        sys.exit(1)


d = LCDSysInfo()
d.display_icon(0, 180 + int(sys.argv[1]) * 38)
