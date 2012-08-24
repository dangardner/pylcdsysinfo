#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from pylcdsysinfo import BackgroundColours, TextColours, TextAlignment, TextLines, LCDSysInfo
from time import sleep

d = LCDSysInfo()
d.clear_lines(TextLines.ALL, BackgroundColours.BLACK)
d.dim_when_idle(False)
d.set_brightness(255)
d.save_brightness(127, 255)
d.set_text_background_colour(BackgroundColours.BLACK)
d.display_cpu_info(8010, 32, TextColours.RED, TextColours.WHITE)
d.display_ram_gpu_info(1994, 32, TextColours.RED, TextColours.GREEN)
d.display_network_info(1, 2, TextColours.RED, TextColours.GREEN, 0, 1) 
d.display_fan_info(1994, 1994, TextColours.RED, TextColours.GREEN)
for pos in range(0, 48):
    d.display_icon(pos, 1 + pos % 32)
d.clear_lines(63, BackgroundColours.WHITE)
d.set_text_background_colour(BackgroundColours.BLUE)
sleep(1)
for line in range(1, 7):
    d.display_text_on_line(line, "Lorem ipsum dolor sit amet, consectetur adipiscing elit.", False, TextAlignment.LEFT, TextColours.WHITE)
