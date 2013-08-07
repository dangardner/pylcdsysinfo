#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import binascii
from pylcdsysinfo import LCDSysInfo

d = LCDSysInfo()
info = d.get_device_info()

def b2h(ba):
    """Convert byte array to hyphen separated hex string."""
    return '-'.join(["%02X" % i for i in ba]).strip()

print """Serial number: %s
Flash Id: %s
EEPROM Data: %s
Device Valid: %s
8Mb Flash: %s
Picture Frame Mode: %s
Flash capacity: %s
Firmware version: %s
Flash data version: %s
""" % (
    b2h(info['serial']),
    b2h(info['flash_id']),
    b2h(info['eeprom']),
    info['device_valid'],
    info['8mb_flash'],
    info['picture_frame_mode'],
    info['flashcap'],
    info['firmware_version'],
    info['flash_data_version'],
),
