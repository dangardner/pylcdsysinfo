#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from pylcdsysinfo import LCDSysInfo, TextAlignment, TextColours, large_image_indexes
from time import sleep

d = LCDSysInfo()
while True:
    for num, idx in enumerate(large_image_indexes):
        d.display_icon(0, idx)
        d.display_text_on_line(1, "{{{" + str(num), False, TextAlignment.NONE, TextColours.WHITE)
        sleep(1)
