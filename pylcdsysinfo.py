# -*- coding: UTF-8 -*-
#
# Interface with LCD Sys info
#
# Some code shamelessly borrowed from https://code.google.com/p/pywws/

import usb, time

font_length_table = [
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
    GREEN       = 1
    YELLOW      = 2
    RED         = 3
    WHITE       = 5
    CYAN        = 6
    LIGHT_GREY  = 7
    DARK_GREY   = 8
    BLACK       = 13
    BROWN       = 15
    BRICK_RED   = 16
    DARK_BLUE   = 17
    LIGHT_BLUE  = 18
    ORANGE      = 21
    PURPLE      = 22
    PINK        = 23
    BRIGHT_WHITE= 24
    GOLD        = 25
    LAVENDER    = 26
    ORANGE_RED  = 27
    MAGENTA     = 28
    YELLOW_ALT  = 29
    NAVY        = 30
    LIGHT_GREEN = 31

""" 16-bit (highcolor) colours """
class Colours(object):
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

class Alignment(object):
    CENTRE      = 0
    LEFT        = 1
    RIGHT       = 2

class LCDSysinfo(object):
    def __init__(self, index=0):
        self.usb_timeout_ms = 2000
        self.clear_lines_wait_ms = 1000

        dev = self._find_device(0x16c0, 0x05dc, index)
        if not dev:
            raise IOError("LCDSysinfo device not found")
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
        if self.devh:
            try:
                self.devh.releaseInterface()
            except ValueError:
                # interface was not claimed, not a problem
                pass

    def _find_device(self, idVendor, idProduct, index):
        for bus in usb.busses():
            for dev in bus.devices:
                if dev.idVendor == idVendor and dev.idProduct == idProduct:
                    index -= 1
                    if index < 0:
                        return dev
        return None

    def change_lcd_brightness(self, value):
        value = min(value, 255)
        self.devh.controlMsg(0x40, 13, "", min(value, 255), min(value, 255), self.usb_timeout_ms)

    def save_brightness_value_to_device(self, off_value, on_value):
        self.devh.controlMsg(0x40, 14, "", off_value + on_value * 256, 0, self.usb_timeout_ms)

    def display_icon_on_grid(self, position, icon_number):
        self.devh.controlMsg(0x40, 27, "", position * 512 + icon_number, 25600, self.usb_timeout_ms)

    def set_text_background_colour(self, colour):
        self.devh.controlMsg(0x40, 30, "", colour, 0, self.usb_timeout_ms)

    def _align_text(self, mm, alignment, screen_px, string_length_px):
        spaces,pixels = divmod(screen_px - string_length_px, 17)
        if alignment == 0: # center
            mm = mm.center(len(mm) + spaces, " ").center(len(mm) + pixels, "{")
        elif alignment == 1: # left
            mm = mm + " " * spaces + "{" * pixels
        elif alignment == 2: # right
            mm = " " * spaces + "{" * pixels + mm
        return mm

    def _text_conversion(self, mm, leavespaceforicon, alignment):
        screen_px = 281 if leavespaceforicon else 319
        mm = mm.strip().replace(" ", "_")
        string_length_px = 0
        for k in range(0, len(mm)):
            ascii_value = ord(mm[k])
            char_length_px = 0
            if ascii_value >= 32 and ascii_value <= 125:
                char_length_px = font_length_table[ascii_value - 32]
            if string_length_px + char_length_px > screen_px:
                mm = mm[0:k]
                break
            string_length_px += char_length_px
        return self._align_text(mm, alignment, screen_px, string_length_px)

    def display_text_on_line(self, line, textstring, leavespaceforicon, alignment, colour):
        textstring = self._text_conversion(textstring, leavespaceforicon, alignment)
        textlength = len(textstring)
        if not leavespaceforicon:
            textlength += 256
        if colour > 32:
            colour = 0
        if line < 1 or line > 6:
            line = 1
        self.devh.controlMsg(0x40, 24, textstring, textlength, (line - 1) * 256 + colour, self.usb_timeout_ms)

    def dim_lcd_during_idle(self, value):
        if value:
            self.devh.controlMsg(0x40, 17, "", 1, 0, self.usb_timeout_ms)
        else:
            self.devh.controlMsg(0x40, 17, "", 0, 266, self.usb_timeout_ms)

    def clear_lines(self, lines, colour):
        # bits 0 - 5 of lines represent each LCD line
        self.devh.controlMsg(0x40, 26, "", lines, colour, self.usb_timeout_ms)
        time.sleep(self.clear_lines_wait_ms / 1000)

    def display_cpu(self, usage, temp, usage_colour=TextColours.GREEN, temp_colour=TextColours.GREEN):
        self.devh.controlMsg(0x40, 21, chr(usage_colour) + chr(temp_colour), usage, temp, self.usb_timeout_ms)
        
    def display_ram_gpu(self, ram, gpu, ram_colour=TextColours.GREEN, gpu_colour=TextColours.GREEN):
        self.devh.controlMsg(0x40, 22, chr(ram_colour) + chr(gpu_colour), ram, gpu, self.usb_timeout_ms)

    def display_network(self, recv, sent, recv_colour=TextColours.GREEN, sent_colour=TextColours.GREEN, recv_mb=0, sent_mb=0):
        self.devh.controlMsg(0x40, 20, chr(recv_mb) + chr(sent_mb) + chr(recv_colour) + chr(sent_colour), recv, sent, self.usb_timeout_ms)

    def display_fans(self, cpufan, chafan, cpufan_colour=TextColours.GREEN, chafan_colour=TextColours.GREEN):
        self.devh.controlMsg(0x40, 23, chr(cpufan_colour) + chr(chafan_colour), cpufan, chafan, self.usb_timeout_ms)
