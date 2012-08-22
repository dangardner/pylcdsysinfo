#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Interface with LCD Sys info
#

import usb, time

USB_TIMEOUT = 2000 # milliseconds
CLEAR_LINES_WAIT = 0.7 # seconds

font_length_table = [
    0x11, 0x06, 0x08, 0x15, 0x0E, 0x19, 0x15, 0x03, 0x08, 0x08, 0x0F, 0x0D, 0x05, 0x08, 0x06, 0x0B, 
    0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x06, 0x06, 0x13, 0x10, 0x13, 0x0C, 
    0x1A, 0x14, 0x10, 0x12, 0x13, 0x0F, 0x0D, 0x13, 0x11, 0x04, 0x07, 0x11, 0x0E, 0x14, 0x11, 0x15, 
    0x0F, 0x15, 0x12, 0x10, 0x13, 0x11, 0x14, 0x1C, 0x13, 0x13, 0x12, 0x07, 0x0B, 0x07, 0x0B, 0x02, 
    0x08, 0x0E, 0x0F, 0x0E, 0x0F, 0x10, 0x0B, 0x0F, 0x0E, 0x04, 0x07, 0x0F, 0x04, 0x18, 0x0E, 0x10, 
    0x0F, 0x0F, 0x0A, 0x0D, 0x0B, 0x0E, 0x10, 0x16, 0x10, 0x10, 0x0E, 0x01, 0x11, 0x02
]

def usb_core_find(idVendor, idProduct):
    busses = usb.busses()

    for bus in busses:
        devices = bus.devices
        for dev in devices:
            if dev.idVendor == idVendor and dev.idProduct == idProduct:
                return dev

    return None

def change_lcd_brightness(dev, value):
    if value > 255:
        value = 255
    dev.controlMsg(0x40, 13, "", value, value, USB_TIMEOUT)

def save_brightness_value_to_device(dev, off_value, on_value):
    dev.controlMsg(0x40, 14, "", off_value + on_value * 256, 0, USB_TIMEOUT)

def turn_off_dimLCD_during_idle(dev):
    dev.controlMsg(0x40, 17, "", 0, 266, USB_TIMEOUT)

def clear_lines(dev, lines, colour):
    # bits 0 - 5 of lines represent each LCD line
    dev.controlMsg(0x40, 26, "", lines, colour, USB_TIMEOUT)
    time.sleep(CLEAR_LINES_WAIT)

# Display the icon icon_number on LCD position
# Position is any value from 0-47 (0 will display in the LCD's upper left
# corner, while 47 will be in the LCD's lower right corner) icon_number is any
# value from 1-32 (This will display 32 different icons which is stored in the
# Flash) Use >257 for user's downloaded icon (Warning: an incorrect icon_number
# will display garbage to LCD). icon 27 is a star.

def display_icon_on_grid(dev, position, icon_number):
    dev.controlMsg(0x40, 27, "", position * 512 + icon_number, 25600, USB_TIMEOUT)
    
def conversion(ds):
    if ds >= 32 and ds <= 125:
        return font_length_table[ds - 32]
    return 0

# alignment - center=0, left=1, right=2
def text_conversion(mm, leavespaceforicon, alignment):
    if leavespaceforicon:
        temp3 = 281
    else:
        temp3 = 319

    mm = mm.strip().replace(" ", "_")
    string_length_px = 0
    for k in range(0, len(mm)):
        char_length_px = conversion(ord(mm[k]))
        if string_length_px + char_length_px > temp3:
            mm = mm[0:k]
            break
        string_length_px += char_length_px
    
    length_remaining = temp3 - string_length_px
    no_of_space = length_remaining / 17
    no_of_pixels = length_remaining % 17
    if alignment == 0: # center
        for k in range(0, no_of_space):
            if k % 2 == 0:
                mm = mm + " "
            else:
                mm = " " + mm
        for k in range(0, no_of_pixels):
            if k % 2 == 0:
                mm = "{" + mm
            else:
                mm = mm + "{"
    elif alignment == 1: # left
        for k in range(0, no_of_space):
            mm += " "
        for k in range(0, no_of_pixels):
            mm += "{"
    elif alignment == 2: # right
        for k in range(0, no_of_space):
            mm = " " + mm
        for k in range(0, no_of_pixels):
            mm = "{" + mm

    return mm

def display_text_on_line(dev, line, textstring, leavespaceforicon, alignment, colour):
    textstring = text_conversion(textstring, leavespaceforicon, alignment)
    temp_2 = len(textstring)
    if not leavespaceforicon:
        temp_2 += 256
    if colour > 32:
        colour = 0
    if line < 1 or line > 6:
        line = 1
    line = line - 1
    temp_3 = line * 256 + colour
    dev.controlMsg(0x40, 24, textstring, temp_2, temp_3, USB_TIMEOUT)

""" Main program starts here """

# find our device
dev = usb_core_find(idVendor=0x16c0, idProduct=0x05dc)

# was it found?
if dev is None:
	raise ValueError('Device not found')

devh = dev.open()

print "Found %s (%s)" % (devh.getString(dev.iProduct, 255), devh.getString(dev.iManufacturer, 255))

devh.setConfiguration(1)
devh.claimInterface(0)

turn_off_dimLCD_during_idle(devh)
change_lcd_brightness(devh, 255)
save_brightness_value_to_device(devh, 0, 255)
clear_lines(devh, 63, 0x0000)
for pos in range(0, 48):
    display_icon_on_grid(devh, pos, 1 + pos % 32)
clear_lines(devh, 63, 0x0000)
for line in range(1, 7):
    display_text_on_line(devh, line, "Hello   world", False, 0, line % 7)
