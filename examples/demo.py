#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from pylcdsysinfo import BackgroundColours, COL2LEFT, TextColours, TextAlignment, TextLines, LCDSysInfo
from time import sleep

d = LCDSysInfo()
d.clear_lines(TextLines.ALL, BackgroundColours.BLACK)
d.dim_when_idle(False)
d.set_brightness(255)
d.save_brightness(127, 255)

# System Info
d.set_text_background_colour(BackgroundColours.BLACK)
d.display_cpu_info(8010, 32, TextColours.RED, TextColours.WHITE)
d.display_ram_gpu_info(1994, 32, TextColours.RED, TextColours.GREEN)
d.display_network_info(1, 2, TextColours.RED, TextColours.GREEN, False, True)
d.display_fan_info(1994, 1994, TextColours.RED, TextColours.GREEN)

# All icons
for pos in range(0, 48):
    d.display_icon(pos, 1 + pos)
sleep(1)

# Arbitrary text drawing
d.clear_lines(TextLines.ALL, BackgroundColours.WHITE)
d.set_text_background_colour(BackgroundColours.BLUE)
for line in range(1, 7):
    d.display_text_on_line(line, "Lorem ipsum dolor sit amet, consectetur adipiscing elit.", False, TextAlignment.LEFT, TextColours.WHITE)
sleep(1)

# Clearing individual lines
for i in range(5,-1,-1):
    d.clear_lines(1 << i, BackgroundColours.BLACK)

# Image Drawing
d.set_text_background_colour(BackgroundColours.BLACK)
d.display_icon(0, 218)

# Multi-color two-column drawing
for line in range(1, 7):
    ipos = (line - 1) * 8
    icon = (line * 2) + 10
    d.display_icon(ipos, icon)
    if line % 2:
        d.display_text_on_line(line, '2-color', True, TextAlignment.RIGHT, TextColours.GREEN)
        d.display_text_on_line(line, 'Slow', True, TextAlignment.LEFT, TextColours.RED, 3)
    else:
        d.display_text_on_line(line, COL2LEFT + 'Drawing', True, TextAlignment.LEFT, TextColours.RED)
        d.display_text_on_line(line, 'Row', True, TextAlignment.RIGHT, TextColours.GREEN, 3)
    d.display_icon(ipos + 4, icon + 1)
sleep(1)

# Refresh the background
d.set_text_background_colour(BackgroundColours.BLACK)
d.display_icon(0, 218)

# Single-color two-column drawing at almost twice the speed
for line in range(1, 7):
    ipos = (line - 1) * 8
    icon = (line * 2) + 10
    if not line == 5:
        d.display_icon(ipos, icon)

    if line == 1:
        d.display_text_on_line(line, 'Two\tcolumn', True, (TextAlignment.RIGHT, TextAlignment.LEFT), TextColours.WHITE)
    elif line == 2:
        d.display_text_on_line(line, 'layout\twith', True, (TextAlignment.LEFT, TextAlignment.RIGHT), TextColours.RED)
    elif line == 3:
        d.display_text_on_line(line, 'only\t\ta', True, (TextAlignment.LEFT, TextAlignment.LEFT), TextColours.YELLOW)
    elif line == 4:
        d.display_text_on_line(line, 'single\tdraw', True, (TextAlignment.RIGHT, TextAlignment.RIGHT), TextColours.GREEN)
    elif line == 5:
        d.display_text_on_line(line, 'call\t\tper', False, TextAlignment.LEFT, TextColours.LIGHT_BLUE)
    else:
        d.display_text_on_line(line, 'text\tline', True, TextAlignment.RIGHT, TextColours.DARK_BLUE)

    if not line == 5:
        d.display_icon(ipos + 4, icon + 1)
