#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function
import sys
from pylcdsysinfo import LCDSysInfo, large_image_indexes

try:
    slot = int(sys.argv[1])
    if not 0 <= slot <= 7:
        raise ValueError("Out of bounds")
except (ValueError, IndexError):
        print("Syntax: %s <0-7>" % (sys.argv[0]), file=sys.stderr)
        sys.exit(1)

d = LCDSysInfo()
d.display_icon(0, large_image_indexes[slot])
