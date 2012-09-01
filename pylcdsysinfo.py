# -*- coding: UTF-8 -*-
#
# Interface with LCD Sys info
#
# Some code shamelessly borrowed from https://code.google.com/p/pywws/

import usb, time

_font_length_table = [
    0x11, 0x06, 0x08, 0x15, 0x0E, 0x19, 0x15, 0x03, 0x08, 0x08, 0x0F, 0x0D,
    0x05, 0x08, 0x06, 0x0B, 0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x11,
    0x11, 0x11, 0x06, 0x06, 0x13, 0x10, 0x13, 0x0C, 0x1A, 0x14, 0x10, 0x12,
    0x13, 0x0F, 0x0D, 0x13, 0x11, 0x04, 0x07, 0x11, 0x0E, 0x14, 0x11, 0x15,
    0x0F, 0x15, 0x12, 0x10, 0x13, 0x11, 0x14, 0x1C, 0x13, 0x13, 0x12, 0x07,
    0x0B, 0x07, 0x0B, 0x02, 0x08, 0x0E, 0x0F, 0x0E, 0x0F, 0x10, 0x0B, 0x0F,
    0x0E, 0x04, 0x07, 0x0F, 0x04, 0x18, 0x0E, 0x10, 0x0F, 0x0F, 0x0A, 0x0D,
    0x0B, 0x0E, 0x10, 0x16, 0x10, 0x10, 0x0E, 0x01, 0x11, 0x02
]

class TextColours(object):
    """Colour palette for text colours"""
    GREEN       = 1
    YELLOW      = 2
    RED         = 3
    WHITE       = 5
    CYAN        = 6
    GREY        = 7
    BLACK       = 13
    BROWN       = 15
    BRICK_RED   = 16
    DARK_BLUE   = 17
    LIGHT_BLUE  = 18
    ORANGE      = 21
    PURPLE      = 22
    PINK        = 23
    PEACH       = 24
    GOLD        = 25
    LAVENDER    = 26
    ORANGE_RED  = 27
    MAGENTA     = 28
    NAVY        = 30
    LIGHT_GREEN = 31

class BackgroundColours(object):
    """Palette of 16-bit (highcolor) background colours"""
    BLACK       = 0x0000
    BLUE        = 0x001f
    GREEN       = 0x07e0
    CYAN        = 0x07ff
    BROWN       = 0x79e0
    DARK_GREY   = 0x7bef
    LIGHT_GREY  = 0xbdf7
    RED         = 0xf800
    PURPLE      = 0xf81f
    ORANGE      = 0xfbe0
    GOLD        = 0xfd20
    YELLOW      = 0xffe0
    WHITE       = 0xffff

class TextAlignment(object):
    """Text alignment specifiers"""
    NONE        = -1
    CENTRE      = 0
    LEFT        = 1
    RIGHT       = 2

class TextLines(object):
    """Text line specifiers"""
    LINE_1      = 1 << 0
    LINE_2      = 1 << 1
    LINE_3      = 1 << 2
    LINE_4      = 1 << 3
    LINE_5      = 1 << 4
    LINE_6      = 1 << 5
    ALL         = LINE_1 + LINE_2 + LINE_3 + LINE_4 + LINE_5 + LINE_6

class LCDSysInfo(object):

    """A Python driver for the Coldtears LCD Sys Info
    (http://coldtearselectronics.wikispaces.com/)
    """

    def __init__(self, index=0):
        """Opens a handle to an LCD Sys Info device.

        Args:
            index (int): The index of the device in the list of connected LCD
                Sys Info devices, with zero (the default) being the first device.
        Raises:
            IOError: An error ocurred while opening the LCD Sys Info device.
            RuntimeError: PyUSB 0.4 or later is required.
        """

        self.usb_timeout_ms = 5000
        self.clear_lines_wait_ms = 1000

        dev = self._find_device(0x16c0, 0x05dc, index)
        if not dev:
            raise IOError("LCD Sys Info device not found")
        self.devh = dev.open()
        if not self.devh:
            raise IOError("Failed to open device")
        try:
            self.devh.claimInterface(0)
        except usb.USBError:
            if not hasattr(self.devh, "detachKernelDriver"):
                raise RuntimeError("Please upgrade python-usb (pyusb) to 0.4 or later")
            try:
                self.devh.detachKernelDriver(0)
                self.devh.claimInterface(0)
            except usb.USBError:
                raise IOError("Failed to claim interface")

    def __del__(self):
        """Closes the handle to the LCD Sys Info device."""
        if self.devh:
            try:
                self.devh.releaseInterface()
            except ValueError:
                # interface was not claimed, not a problem
                pass

    def _find_device(self, idVendor, idProduct, index):
        """Locate the index'th device with specified vendor and product id."""
        for bus in usb.busses():
            for dev in bus.devices:
                if dev.idVendor == idVendor and dev.idProduct == idProduct:
                    index -= 1
                    if index < 0:
                        return dev
        return None

    def set_brightness(self, value):
        """Set the brightness of the LCD backlight without saving the value to the device.

        Args:
            value (int): Number representing the LCD brightness, in the range 0 to 255.
        """
        value = max(0, min(value, 255))
        self.devh.controlMsg(0x40, 13, "", min(value, 255), min(value, 255), self.usb_timeout_ms)

    def save_brightness(self, off_value, on_value):
        """Set the brightness of the LCD backlight when idle and active and
        save the values to the device.

        Args:
            off_value (int): Number representing the LCD backlight brightness
                when the LCD is idle.
            on_value (int): Number representing the LCD backlight brightness
                when the LCD is active.
        """
        self.devh.controlMsg(0x40, 14, "", off_value + on_value * 256, 0, self.usb_timeout_ms)

    def display_icon(self, position, icon_number):
        """Display an icon at a specified position on the device.

        Args:
            position (int): Number representing the position in which to display 
                the icon, in the range 0 to 47, where 0 is the top-left corner
                of the display and 48 is the bottom-right corner.
            icon_number (int): The index of the icon to be displayed. This may be
                in the range 1 to 32 for the default icons or 257+ for downloaded
                icons. An invalid icon number will display garbage to screen.
        """
        # TODO create enumeration class for icons
        position = max(0, min(position, 47))
        self.devh.controlMsg(0x40, 27, "", position * 512 + icon_number, 25600, self.usb_timeout_ms)

    def set_text_background_colour(self, colour):
        """Set the background colour for text display.

        Args:
            colour (int): The background colour from pylcdsysinfo.BackgroundColours.
        """
        self.devh.controlMsg(0x40, 30, "", colour, 0, self.usb_timeout_ms)

    def _align_text(self, mm, alignment, screen_px, string_length_px):
        """Align text suitably for the specified screen width"""
        spaces,pixels = divmod(screen_px - string_length_px, 17)
        if alignment == TextAlignment.CENTRE:
            mm = mm.center(len(mm) + spaces, " ").center(len(mm) + pixels, "{")
        elif alignment == TextAlignment.LEFT:
            mm = mm + " " * spaces + "{" * pixels
        elif alignment == TextAlignment.RIGHT:
            mm = " " * spaces + "{" * pixels + mm
        return mm

    def _text_conversion(self, mm, pad_for_icon, alignment):
        """Pad, truncate, align and otherwise munge the specified text."""
        screen_px = 281 if pad_for_icon else 319
        mm = mm.strip().replace(" ", "___")
        string_length_px = 0
        for k in range(0, len(mm)):
            ascii_value = ord(mm[k])
            char_length_px = 0
            if ascii_value >= 32 and ascii_value <= 125:
                char_length_px = _font_length_table[ascii_value - 32]
            if string_length_px + char_length_px > screen_px:
                mm = mm[0:k]
                break
            string_length_px += char_length_px
        return self._align_text(mm, alignment, screen_px, string_length_px)

    def display_text_on_line(self, line, text_string, pad_for_icon, alignment, colour):
        """Display text on a line of the device.

        Args:
            line (int): The line on which the text should be displayed, in the range 1 to 6.
            text_string (str): The text to be displayed, which will be truncated as
                required. Use "|" for wider spacing and "^" to display a "degrees" symbol.
            pad_for_icon (bool): If true, padding will be added to the left of the text,
                to accommodate an icon.
            alignment (int): The text alignment from pylcdsysinfo.TextAlignment.
            colour (int): The text colour from pylcdsysinfo.TextColours.
        """
        text_string = self._text_conversion(text_string, pad_for_icon, alignment) + chr(0)
        text_length = len(text_string)
        if not pad_for_icon:
            text_length += 256
        colour = min(colour, 32)
        line = max(1, min(line, 6))
        self.devh.controlMsg(0x40, 24, text_string, text_length, (line - 1) * 256 + colour,
            self.usb_timeout_ms)

    def dim_when_idle(self, value):
        """Set whether to dim the LCD backlight after the device has been idle for 10 seconds.

        Args:
            value (bool): If true, the LCD backlight will dim when the device is idle,
                otherwise the function will be disabled.
        """
        if value:
            self.devh.controlMsg(0x40, 17, "", 1, 0, self.usb_timeout_ms)
        else:
            self.devh.controlMsg(0x40, 17, "", 0, 266, self.usb_timeout_ms)

    def clear_lines(self, lines, colour):
        """Clear lines of the display using a coloured background.

        Args:
            lines (int): A number representing the lines to be cleared, using the
                values from pylcdsysinfo.TextLines OR'd together to form bits 0 to 5.
            colour (int): The background colour from pylcdsysinfo.BackgroundColours.
        """
        lines = max(1, min(lines, 63))
        self.devh.controlMsg(0x40, 26, "", lines, colour, self.usb_timeout_ms)
        time.sleep(self.clear_lines_wait_ms / 1000)

    def display_cpu_info(self, cpu_util, cpu_temp, util_colour=TextColours.GREEN, temp_colour=TextColours.GREEN):
        """Display CPU utilisation and temperature information.

        Args:
            cpu_util (int): Percentage CPU utilisation, to a maximum of 4 digits,
                e.g. 994 will display 99.4%.
            cpu_temp (int): CPU temperature in degrees Celsius, to a maximum of 2 digits,
                e.g. 32 will display 32°C.
            util_colour (int): The colour of the CPU utilitisation, from
                pylcdsysinfo.BackgroundColours (defaults to GREEN).
            temp_colour (int): The colour of the CPU temperature, from
                pylcdsysinfo.BackgroundColours (defaults to GREEN).
        """
        self.devh.controlMsg(0x40, 21, chr(util_colour) + chr(temp_colour), cpu_util, cpu_temp, self.usb_timeout_ms)

    def display_ram_gpu_info(self, ram, gpu_temp, ram_colour=TextColours.GREEN, temp_colour=TextColours.GREEN):
        """Display available RAM and GPU temperature information.

        Args:
            ram (int): Available RAM in megabytes, to a maximum of 4 digits,
                e.g. 1994 will display 1994Mb.
            gpu_temp (int): GPU temperature in degrees Celsius, to a maximum of 2 digits,
                e.g. 32 will display 32°C.
            util_colour (int): The colour of the available RAM, from
                pylcdsysinfo.BackgroundColours (defaults to GREEN).
            temp_colour (int): The colour of the GPU temperature, from
                pylcdsysinfo.BackgroundColours (defaults to GREEN).
        """
        self.devh.controlMsg(0x40, 22, chr(ram_colour) + chr(temp_colour), ram, gpu_temp, self.usb_timeout_ms)

    def display_network_info(self, recv, sent, recv_colour=TextColours.GREEN, sent_colour=TextColours.GREEN, recv_mb=False, sent_mb=False):
        """Display network utilisation information.

        Args:
            recv (int): Current network receive rate, to a maximum of 4 digits,
                e.g. 1994 will display 1994Mb.
            sent (int): Current network transmit rate, to a maximum of 4 digits,
                e.g. 1994 will display 1994Mb.
            recv_colour (int): The colour of the network receive rate, from
                pylcdsysinfo.BackgroundColours (defaults to GREEN).
            sent_colour (int): The colour of the network transmit rate, from
                pylcdsysinfo.BackgroundColours (defaults to GREEN).
            recv_mb (bool): Display receive rate in kb instead of the default Mb.
            sent_mb (bool): Display transmit rate in kb instead of the default Mb.
        """
        self.devh.controlMsg(0x40, 20, chr(recv_mb) + chr(sent_mb) + chr(recv_colour) + chr(sent_colour), recv, sent, self.usb_timeout_ms)

    def display_fan_info(self, cpufan, chafan, cpufan_colour=TextColours.GREEN, chafan_colour=TextColours.GREEN):
        """Display fan speed information.

        Args:
            cpufan (int): Current CPU fan speed, to a maximum of 4 digits,
                e.g. 1994 will display 1994rpm.
            chafan (int): Current chassis fan speed, to a maximum of 4 digits,
                e.g. 1994 will display 1994rpm.
            cpufan_colour (int): The colour of the CPU fan speed, from
                pylcdsysinfo.BackgroundColours (defaults to GREEN).
            chafan_colour (int): The colour of the chassis fan speed, from
                pylcdsysinfo.BackgroundColours (defaults to GREEN).
        """
        self.devh.controlMsg(0x40, 23, chr(cpufan_colour) + chr(chafan_colour), cpufan, chafan, self.usb_timeout_ms)
