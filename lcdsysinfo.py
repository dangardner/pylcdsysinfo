#!/usr/bin/env python
#
# Interface with LCD Sys info
#

import usb
from time import sleep

USB_TIMEOUT = 1000

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

# Display the icon icon_number on LCD position
# Position is any value from 0-47 (0 will display in the LCD's upper left
# corner, while 47 will be in the LCD's lower right corner) icon_number is any
# value from 1-32 (This will display 32 different icons which is stored in the
# Flash) Use >257 for user's downloaded icon (Warning: an incorrect icon_number
# will display garbage to LCD). icon 27 is a star.

def display_icon_on_grid(dev, position, icon_number):
    dev.controlMsg(0x40, 27, "", position * 512 + icon_number, 25600, USB_TIMEOUT)
    
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
clear_lines(devh, 10, 0xf800)
for pos in range(0, 48):
    display_icon_on_grid(devh, pos, 1 + pos % 32)
    print "Displaying icon %d at position %d" % (1 + pos % 32, pos)
