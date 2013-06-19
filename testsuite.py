#!/usr/bin/env python
# -*- coding: ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
"""Test suite for LCD routines"""

import os
import sys

try:
    if sys.version_info < (2, 3):
        # unittest2 does NOT work under Python 2.2.
        raise ImportError
    import unittest2
    unittest = unittest2
except ImportError:
    import unittest
    unittest2 = None

import pylcdsysinfo


IMAGE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(IMAGE_DIR, 'images')
IMAGE_320X240_DIR = os.path.join(IMAGE_DIR, '320x240')
ICON_DIR = os.path.join(IMAGE_DIR, 'icons')


class ImageTests(unittest.TestCase):

    def skip(self, reason):
        """Skip current test because of `reason`.

        NOTE expects unittest2, and defaults to "pass" if not available.
        """
        if unittest2:
            raise unittest2.SkipTest(reason)

    def testimage_pattern_320x240_rgb565_bmp(self):
        filename = 'testpattern_rgb565.bmp'
        filename = os.path.join(IMAGE_320X240_DIR, filename)
        canon_filename = os.path.splitext(filename)[0] + '.raw'

        f = open(filename, 'rb')
        data = f.read()
        f.close()
        raw_data = pylcdsysinfo._bmp_to_raw(data)

        f = open(canon_filename, 'rb')
        canon_data = f.read()
        f.close()
        self.assertEqual(canon_data, raw_data, 'does not match canon')

    def testimage_pattern_320x240_rgb888_png(self):
        filename = 'testpattern.png'
        """NOTE the rgb888 -> rgb565  conversion implemented in ffmeg is
        slightly different to the technique applied in image_to_raw().
        This is why a different raw file is used, also testpattern_rgb565.bmp
        is already in rgb565 format, the png is full 16/24 bit depth.
        """
        filename = os.path.join(IMAGE_320X240_DIR, filename)
        canon_filename = os.path.splitext(filename)[0] + '.raw'

        im = pylcdsysinfo.Image.open(filename)
        raw_data = pylcdsysinfo.image_to_raw(im)

        f = open(canon_filename, 'rb')
        canon_data = f.read()
        f.close()
        self.assertEqual(canon_data, raw_data, 'does not match canon')


if __name__ == '__main__':
    unittest.main()
