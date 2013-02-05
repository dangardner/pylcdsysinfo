pylcdsysinfo
============

Python interface to Coldtears' LCD Sys Info device (http://www.coldtears.com/electronics/)

**Note:** You may need to copy the provided `99-lcdsysinfo.rules` file into
`/etc/udev/rules.d/` in order to grant pylcdsysinfo permission to claim the
device without running as root.

Help on module pylcdsysinfo:

    NAME
        pylcdsysinfo

    FILE
        pylcdsysinfo.py

    DESCRIPTION
        # -*- coding: UTF-8 -*-
        #
        # Interface with LCD Sys info USB device
        #
        # Copyright (C) 2012  Dan Gardner
        #
        # USB initialisation code has been adapted from pywws by Jim Easterbrook
        #
        # This program is free software: you can redistribute it and/or modify
        # it under the terms of the GNU General Public License as published by
        # the Free Software Foundation, either version 3 of the License, or
        # (at your option) any later version.
        #
        # This program is distributed in the hope that it will be useful,
        # but WITHOUT ANY WARRANTY; without even the implied warranty of
        # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
        # GNU General Public License for more details.
        #
        # See <http://www.gnu.org/licenses/gpl-3.0.txt>

    CLASSES
        __builtin__.object
            BackgroundColours
            LCDSysInfo
            TextAlignment
            TextColours
            TextLines

        class BackgroundColours(__builtin__.object)
         |  Palette of 16-bit (highcolor) background colours
         |
         |  Data descriptors defined here:
         |
         |  __dict__
         |      dictionary for instance variables (if defined)
         |
         |  __weakref__
         |      list of weak references to the object (if defined)
         |
         |  ----------------------------------------------------------------------
         |  Data and other attributes defined here:
         |
         |  BLACK = 0
         |
         |  BLUE = 31
         |
         |  BROWN = 31200
         |
         |  CYAN = 2047
         |
         |  DARK_GREY = 31727
         |
         |  GOLD = 64800
         |
         |  GREEN = 2016
         |
         |  LIGHT_GREY = 48631
         |
         |  ORANGE = 64480
         |
         |  PURPLE = 63519
         |
         |  RED = 63488
         |
         |  WHITE = 65535
         |
         |  YELLOW = 65504

        class LCDSysInfo(__builtin__.object)
         |  A Python driver for the Coldtears LCD Sys Info
         |  (http://coldtearselectronics.wikispaces.com/)
         |
         |  Methods defined here:
         |
         |  __del__(self)
         |      Closes the handle to the LCD Sys Info device.
         |
         |  __init__(self, index=0)
         |      Opens a handle to an LCD Sys Info device.
         |
         |      Args:
         |          index (int): The index of the device in the list of connected LCD
         |              Sys Info devices, with zero (the default) being the first device.
         |      Raises:
         |          IOError: An error ocurred while opening the LCD Sys Info device.
         |          RuntimeError: PyUSB 0.4 or later is required.
         |
         |  clear_lines(self, lines, colour)
         |      Clear lines of the display using a coloured background.
         |
         |      Args:
         |          lines (int): A number representing the lines to be cleared, using the
         |              values from pylcdsysinfo.TextLines OR'd together to form bits 0 to 5.
         |          colour (int): The background colour from pylcdsysinfo.BackgroundColours.
         |
         |  dim_when_idle(self, value)
         |      Set whether to dim the LCD backlight after the device has been idle for 10 seconds.
         |
         |      Args:
         |          value (bool): If true, the LCD backlight will dim when the device is idle,
         |              otherwise the function will be disabled.
         |
         |  display_cpu_info(self, cpu_util, cpu_temp, util_colour=1, temp_colour=1)
         |      Display CPU utilisation and temperature information.
         |
         |      Args:
         |          cpu_util (int): Percentage CPU utilisation, to a maximum of 4 digits,
         |              e.g. 994 will display 99.4%.
         |          cpu_temp (int): CPU temperature in degrees Celsius, to a maximum of 2 digits,
         |              e.g. 32 will display 32°C.
         |          util_colour (int): The colour of the CPU utilitisation, from
         |              pylcdsysinfo.BackgroundColours (defaults to GREEN).
         |          temp_colour (int): The colour of the CPU temperature, from
         |              pylcdsysinfo.BackgroundColours (defaults to GREEN).
         |
         |  display_fan_info(self, cpufan, chafan, cpufan_colour=1, chafan_colour=1)
         |      Display fan speed information.
         |
         |      Args:
         |          cpufan (int): Current CPU fan speed, to a maximum of 4 digits,
         |              e.g. 1994 will display 1994rpm.
         |          chafan (int): Current chassis fan speed, to a maximum of 4 digits,
         |              e.g. 1994 will display 1994rpm.
         |          cpufan_colour (int): The colour of the CPU fan speed, from
         |              pylcdsysinfo.BackgroundColours (defaults to GREEN).
         |          chafan_colour (int): The colour of the chassis fan speed, from
         |              pylcdsysinfo.BackgroundColours (defaults to GREEN).
         |
         |  display_icon(self, position, icon_number)
         |      Display an icon at a specified position on the device.
         |
         |      Args:
         |          position (int): Number representing the position in which to display
         |              the icon, in the range 0 to 47, where 0 is the top-left corner
         |              of the display and 48 is the bottom-right corner.
         |          icon_number (int): The index of the icon to be displayed. This may be
         |              in the range 1 to 32 for the default icons or 257+ for downloaded
         |              icons. An invalid icon number will display garbage to screen.
         |
         |  display_network_info(self, recv, sent, recv_colour=1, sent_colour=1, recv_mb=False, sent_mb=False)
         |      Display network utilisation information.
         |
         |      Args:
         |          recv (int): Current network receive rate, to a maximum of 4 digits,
         |              e.g. 1994 will display 1994Mb.
         |          sent (int): Current network transmit rate, to a maximum of 4 digits,
         |              e.g. 1994 will display 1994Mb.
         |          recv_colour (int): The colour of the network receive rate, from
         |              pylcdsysinfo.BackgroundColours (defaults to GREEN).
         |          sent_colour (int): The colour of the network transmit rate, from
         |              pylcdsysinfo.BackgroundColours (defaults to GREEN).
         |          recv_mb (bool): Display receive rate in kb instead of the default Mb.
         |          sent_mb (bool): Display transmit rate in kb instead of the default Mb.
         |
         |  display_ram_gpu_info(self, ram, gpu_temp, ram_colour=1, temp_colour=1)
         |      Display available RAM and GPU temperature information.
         |
         |      Args:
         |          ram (int): Available RAM in megabytes, to a maximum of 4 digits,
         |              e.g. 1994 will display 1994Mb.
         |          gpu_temp (int): GPU temperature in degrees Celsius, to a maximum of 2 digits,
         |              e.g. 32 will display 32°C.
         |          util_colour (int): The colour of the available RAM, from
         |              pylcdsysinfo.BackgroundColours (defaults to GREEN).
         |          temp_colour (int): The colour of the GPU temperature, from
         |              pylcdsysinfo.BackgroundColours (defaults to GREEN).
         |
         |  display_text_on_line(self, line, text_string, pad_for_icon, alignment, colour, field_length=8)
         |      Display text on a line of the device.
         |
         |      Args:
         |          line (int): The line on which the text should be displayed, in the range 1 to 6.
         |          text_string (str): The text to be displayed, which will be truncated as
         |              required. Use "|" for wider spacing and "^" to display a "degrees" symbol.
         |              Use "\t" (TAB) to construct a two-column layout.
         |          pad_for_icon (bool): If true, padding will be added to the left of the text,
         |              to accommodate an icon.
         |          alignment (int): The text alignment from pylcdsysinfo.TextAlignment.
         |              May be a list/tuple with two values if texxt_string contains "\t".
         |          colour (int): The text colour from pylcdsysinfo.TextColours.
         |          field_length (int): If provided, limits the size of the region in
         |              which left/center/right alignment applies to the specified
         |              number of icon widths. Ignored if text_string contains "\t".
         |
         |  get_device_info(self)
         |      Retrieve device information.
         |
         |  save_brightness(self, off_value, on_value)
         |      Set the brightness of the LCD backlight when idle and active and
         |      save the values to the device.
         |
         |      Args:
         |          off_value (int): Number representing the LCD backlight brightness
         |              when the LCD is idle.
         |          on_value (int): Number representing the LCD backlight brightness
         |              when the LCD is active.
         |
         |  send_command_to_flash(self, address, command)
         |      Send command to SPI flash memory.
         |
         |      Args:
         |          address (int): Address of sector or page to write
         |          command (int): 0=write enable, 1=write disable, 2=erase sector, 3=program page.
         |
         |  set_brightness(self, value)
         |      Set the brightness of the LCD backlight without saving the value to the device.
         |
         |      Args:
         |          value (int): Number representing the LCD brightness, in the range 0 to 255.
         |
         |  set_text_background_colour(self, colour)
         |      Set the background colour for text display.
         |
         |      Args:
         |          colour (int): The background colour from pylcdsysinfo.BackgroundColours.
         |
         |  write_image_to_flash(self, sector, bitmap)
         |      Write bitmap image to SPI flash memory.
         |
         |      Args:
         |          sector (int): Address of starting sector (0-511).
         |          bitmap (str): Contents of bitmap image, in 16bpp, RGB 5:6:5 format.
         |
         |  ----------------------------------------------------------------------
         |  Data descriptors defined here:
         |
         |  __dict__
         |      dictionary for instance variables (if defined)
         |
         |  __weakref__
         |      list of weak references to the object (if defined)

        class TextAlignment(__builtin__.object)
         |  Text alignment specifiers
         |
         |  Data descriptors defined here:
         |
         |  __dict__
         |      dictionary for instance variables (if defined)
         |
         |  __weakref__
         |      list of weak references to the object (if defined)
         |
         |  ----------------------------------------------------------------------
         |  Data and other attributes defined here:
         |
         |  CENTRE = 0
         |
         |  LEFT = 1
         |
         |  NONE = -1
         |
         |  RIGHT = 2

        class TextColours(__builtin__.object)
         |  Colour palette for text colours
         |
         |  Data descriptors defined here:
         |
         |  __dict__
         |      dictionary for instance variables (if defined)
         |
         |  __weakref__
         |      list of weak references to the object (if defined)
         |
         |  ----------------------------------------------------------------------
         |  Data and other attributes defined here:
         |
         |  BLACK = 13
         |
         |  BRICK_RED = 16
         |
         |  BROWN = 15
         |
         |  CYAN = 6
         |
         |  DARK_BLUE = 17
         |
         |  GOLD = 25
         |
         |  GREEN = 1
         |
         |  GREY = 7
         |
         |  LAVENDER = 26
         |
         |  LIGHT_BLUE = 18
         |
         |  LIGHT_GREEN = 31
         |
         |  MAGENTA = 28
         |
         |  NAVY = 30
         |
         |  ORANGE = 21
         |
         |  ORANGE_RED = 27
         |
         |  PEACH = 24
         |
         |  PINK = 23
         |
         |  PURPLE = 22
         |
         |  RED = 3
         |
         |  WHITE = 5
         |
         |  YELLOW = 2

        class TextLines(__builtin__.object)
         |  Text line specifiers
         |
         |  Data descriptors defined here:
         |
         |  __dict__
         |      dictionary for instance variables (if defined)
         |
         |  __weakref__
         |      list of weak references to the object (if defined)
         |
         |  ----------------------------------------------------------------------
         |  Data and other attributes defined here:
         |
         |  ALL = 63
         |
         |  LINE_1 = 1
         |
         |  LINE_2 = 2
         |
         |  LINE_3 = 4
         |
         |  LINE_4 = 8
         |
         |  LINE_5 = 16
         |
         |  LINE_6 = 32
