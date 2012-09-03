#!/usr/bin/env python

import sys, os
from pylcdsysinfo import LCDSysInfo, TextAlignment, TextColours

def usage():
    print >>sys.stderr, "Usage: %s <icon 1-42> <imagefile>" % (sys.argv[0])
    sys.exit(1)

if len(sys.argv) != 3:
    usage()

try:
    if int(sys.argv[1]) < 1 or int(sys.argv[1]) > 42:
        raise ValueError("Out of bounds")
except ValueError:
    usage()

infile = sys.argv[2]

if not os.path.isfile(infile):
    print >>sys.stderr, "No such file '%s'" % (infile)
    sys.exit(1)

# Hack - redirect stderr to /dev/null to prevent noisy ffmpeg output
bmpfile = os.popen("ffmpeg -f image2 -i %s -vcodec bmp -pix_fmt rgb565 -f image2 - 2>/dev/null" % (infile)).read()

d = LCDSysInfo()
d.write_image_to_flash(int(sys.argv[1]), bmpfile)
