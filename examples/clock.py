#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""Dumb clock"""

import os
import sys
import math
import time
import datetime

from pylcdsysinfo import LCDSysInfo, TextLines, TextLines, BackgroundColours, TextColours


def clock_loop(bg=None, fg=None):
    update_display_period = 1  # number of seconds to wait before updating display
    floor = math.floor  # minor optimization
    
    if bg is None:
        bg = BackgroundColours.BLACK
    if fg is None:
        fg = TextColours.GREEN
    
    line_num = 3

    d = LCDSysInfo()
    d.clear_lines(TextLines.ALL, bg)
    d.dim_when_idle(False)
    d.set_brightness(127)
    d.save_brightness(127, 255)
    d.set_text_background_colour(bg)

    while 1:
        clock_str = str(datetime.datetime.now()).split('.')[0]
        d.display_text_on_line(line_num, clock_str, False, None, fg)
        
        # Work out when to wake up for the next round/whole (non-fractional) time
        start_time = time.time()
        future_time = floor(start_time) + update_display_period  # pure float math
        sleep_time = future_time - start_time
        time.sleep(sleep_time)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    
    clock_loop()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
