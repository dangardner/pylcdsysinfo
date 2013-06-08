#!/usr/bin/env python
# -*- coding: ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
# Interface with Cold Tears LCD Sys info USB device
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
"""Example usage:

    ./setup.py install
    ./setup.py sdist

"""

from distutils.core import setup

import pylcdsysinfo

print pylcdsysinfo.version_info
print pylcdsysinfo.__version__

setup(
    name='pylcdsysinfo',
    version=pylcdsysinfo.__version__,
    description='Python Cold Tears LCD Sys info USB device api',
    author='Dan Gardner',
    author_email='?',  # FIXME
    license = 'GPL3',
    url='http://github.com/dangardner/pylcdsysinfo',
    py_modules=['pylcdsysinfo',],  # TODO convert to a package, see below
    #packages=['pylcdsysinfo',],
    long_description =
"""pylcdsysinfo offers easy access to the Cold Tears LCD Sys info USB device from Python.
"""
)
