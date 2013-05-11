#!/usr/bin/env python

from __future__ import print_function
import sys, os, subprocess
from pylcdsysinfo import LCDSysInfo, TextAlignment, TextColours

def usage():
    print("Usage: %s <icon 1-42> <imagefile>" % (sys.argv[0]), file=sys.stderr)
    sys.exit(1)

if len(sys.argv) != 3:
    usage()

try:
    slot = int(sys.argv[1])
    if not 0 < slot <= 42:
        raise ValueError("Out of bounds")
except (ValueError, IndexError):
    usage()

infile = sys.argv[2]

if not os.path.isfile(infile):
    print("No such file '%s'" % (infile), file=sys.stderr)
    sys.exit(1)

# Hack - redirect stderr to /dev/null to prevent noisy ffmpeg output
bmpfile = subprocess.Popen("ffmpeg -f image2 -i %s -vcodec bmp -pix_fmt rgb565 -f image2 - 2>/dev/null" % (infile),
    shell=True, stdout=subprocess.PIPE).stdout.read()

d = LCDSysInfo()
d.write_image_to_flash(slot, bmpfile)
