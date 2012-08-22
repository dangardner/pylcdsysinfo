#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pylcdsysinfo

d = pylcdsysinfo.LCDSysinfo()
d.dim_lcd_during_idle(False)
d.change_lcd_brightness(255)
d.save_brightness_value_to_device(0, 255)
d.clear_lines(63, 0x0000)
for pos in range(0, 48):
    d.display_icon_on_grid(pos, 1 + pos % 32)
d.clear_lines(63, 0x0000)
for line in range(1, 7):
    d.display_text_on_line(line, "Hello  world", False, line % 3, line % 7)
