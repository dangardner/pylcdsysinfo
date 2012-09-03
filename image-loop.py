#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from pylcdsysinfo import LCDSysInfo, TextAlignment, TextColours
from time import sleep

d = LCDSysInfo()
while True:
    for c in range(0, 8):
        dest = 180 + (c * 38)
        d.display_icon(0, dest)
        d.display_text_on_line(1, "{{{" + str(c), False, TextAlignment.NONE, TextColours.WHITE)
        sleep(1)
