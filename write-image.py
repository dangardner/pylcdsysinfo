#!/usr/bin/env python

import sys, os
from pylcdsysinfo import LCDSysInfo, TextAlignment, TextColours

def usage():
    print "Usage: %s <inputfile> <sector>" % (sys.argv[0])
    sys.exit(1)

def leUnpack(byte):
    """ Converts byte string to integer. Use Little-endian byte order."""
    return sum([
        ord(b) << (8 * i) for i, b in enumerate(byte)
    ])

# TODO Use PIL to convert to 24bpp bitmap, then convert to rgb565 using
# this function, instead of using ffmpeg
def to565(r,g,b):
    return ((((r) >> 3) << 11) | (((g) >> 2) << 5) | ((b) >> 3))
    
if len(sys.argv) != 3:
    usage()

infile = sys.argv[1]

try:
    sector = int(sys.argv[2])
except ValueError:
    print "Sector must be an integer"
    sys.exit(1)

if not os.path.isfile(infile):
    print "No such file '%s'" % (infile)
    sys.exit(1)

# Hack - redirect stderr to /dev/null to prevent noisy ffmpeg output
bmpfile = os.popen("ffmpeg -f image2 -i %s -vcodec bmp -pix_fmt rgb565 -f image2 - 2>/dev/null" % (infile)).read()

d = LCDSysInfo()
d.write_image_to_flash(bmpfile, sector)
