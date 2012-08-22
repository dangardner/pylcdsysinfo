#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from pylcdsysinfo import Colours, TextColours, Alignment, LCDSysinfo

d = LCDSysinfo()
d.dim_lcd_during_idle(False)
d.change_lcd_brightness(255)
d.save_brightness_value_to_device(0, 255)
d.clear_lines(63, Colours.BLACK)
d.set_text_background_colour(Colours.BLACK)
d.display_cpu(994, 32, TextColours.BRIGHT_WHITE, TextColours.WHITE)
d.display_ram_gpu(1994, 32, TextColours.RED, TextColours.GREEN)
d.display_network(1994, 1994, TextColours.RED, TextColours.GREEN, 0, 1) 
d.display_fans(1994, 1994, TextColours.RED, TextColours.GREEN)
for pos in range(0, 48):
    d.display_icon_on_grid(pos, 1 + pos % 32)
d.clear_lines(63, Colours.WHITE)
d.set_text_background_colour(Colours.ORANGE)
for line in range(1, 7):
    d.display_text_on_line(line, "Hello|world", False, Alignment.LEFT, TextColours.GREEN)
