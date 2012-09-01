#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from pylcdsysinfo import LCDSysInfo, TextAlignment, TextColours

d = LCDSysInfo()
c = 1
for dest in (180, 218, 256, 294, 332, 370, 408, 446):
    d.display_text_on_line(3, "Image " + str(c), False, TextAlignment.CENTRE, TextColours.WHITE)
    d.display_icon(0, dest)
    c += 1
