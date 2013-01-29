#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from pylcdsysinfo import BackgroundColours, COL2LEFT, TextColours, TextAlignment, TextLines, LCDSysInfo
from time import sleep

d = LCDSysInfo()
d.clear_lines(TextLines.ALL, BackgroundColours.BLACK)
d.dim_when_idle(False)
d.set_brightness(255)
d.save_brightness(127, 255)
d.set_text_background_colour(BackgroundColours.BLACK)
d.display_cpu_info(8010, 32, TextColours.RED, TextColours.WHITE)
d.display_ram_gpu_info(1994, 32, TextColours.RED, TextColours.GREEN)
d.display_network_info(1, 2, TextColours.RED, TextColours.GREEN, False, True)
d.display_fan_info(1994, 1994, TextColours.RED, TextColours.GREEN)
for pos in range(0, 48):
    d.display_icon(pos, 1 + pos % 32)
d.clear_lines(TextLines.ALL, BackgroundColours.WHITE)
d.set_text_background_colour(BackgroundColours.BLUE)
sleep(1)
for line in range(1, 7):
    d.display_text_on_line(line, "Lorem ipsum dolor sit amet, consectetur adipiscing elit.", False, TextAlignment.LEFT, TextColours.WHITE)
sleep(1)
d.clear_lines(TextLines.ALL, BackgroundColours.BLACK)
d.set_text_background_colour(BackgroundColours.BLACK)
d.display_icon(0, 218)
for line in range(1, 7):
    ipos = (line - 1) * 8
    icon = (line * 2) + 10
    d.display_icon(ipos, icon)
    if line % 2:
        d.display_text_on_line(line, 'Right', True, TextAlignment.RIGHT, TextColours.GREEN)
        d.display_text_on_line(line, 'Left', True, TextAlignment.LEFT, TextColours.RED, 3)
    else:
        d.display_text_on_line(line, COL2LEFT + 'Left', True, TextAlignment.LEFT, TextColours.RED)
        d.display_text_on_line(line, 'Right', True, TextAlignment.RIGHT, TextColours.GREEN, 3)
    d.display_icon(ipos + 4, icon + 1)
