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
"""Please use pip to install http://www.pip-installer.org/

Examples of pip usage:

    pip install git+https://github.com/clach04/pylcdsysinfo.git@add_setup_py
    pip install -r requirements.txt

Example setup.py usage:

    ./setup.py install
    ./setup.py sdist

"""

try:
    import setuptools
    from setuptools import setup
except ImportError:
    setuptools = None
    from distutils.core import setup

import pylcdsysinfo


kwargs = {
    'requires': [
        # NOTE pyusb>=0.4 does work but later version 1.0 releases are
        # needed for to avoid crashes on device removal under Windows
        'pyusb (>=1.0.0a3)',
    ],
}

if setuptools:
    kwargs['install_requires'] = [
            # NOTE pyusb>=0.4 does work but later version 1.0 releases are
            # needed for to avoid crashes on device removal under Windows
            'pyusb>=1.0.0a3',
        ]

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
""",
    **kwargs
)
