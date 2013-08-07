pylcdsysinfo
============

Python interface to Coldtears Electronics LCD Sys Info device (http://coldtearselectronics.wikispaces.com/)

## Installation

**Note:** On some Linux platforms like Ubuntu, only root has write permission to USB devices unless permission is is given to other users.
You may need to copy the provided `99-lcdsysinfo.rules` file into
`/etc/udev/rules.d/` in order to grant pylcdsysinfo permission to claim the device without running as root. 

Example:

    sudo cp 99-lcdsysinfo.rules /etc/udev/rules.d/

If the screen is already plugged in, unplug and plug back in again after copying the udev rules file.

pylcdsysinfo relies on the Python USB library http://pyusb.sourceforge.net/ - this can be installed via pip/easy_install

Example:

    pip install pyusb

or through the distribution specific package install, example for Ubuntu/Debian:

    sudo apt-get install python-usb

**Note:** using the operating system packages is likely to install an old version.

For Windows an additional step is required, a USB driver is required to allow the Python USB library to talk with the display. A signed driver for Windows 7 (and XP) 64 and 32 bit can be installed by using zadig_v2.0.1.160 from http://sourceforge.net/projects/libwdi/files/zadig/ 

Ensure the LCD device is **not** plugged in, run zadig, insert the device, change the driver to `libusb-win32` and hit install. libusb-win32 version 1.2.4.0 from http://sourceforge.net/projects/libusb-win32/files/libusb-win32-releases/1.2.4.0/ is also known to work under Windows XP, with Python 2.6.4 and Python USB 1.0.

On OS X, it is most straightforward to use the [homebrew](http://brew.sh/) package manager to install the dependencies (libusb and pyusb).

    brew install libusb python
    pip install pyusb

## Usage

For help on usage of the pylcdsysinfo module and API, see the file `USAGE.txt` (pydoc)

## Tools and examples

 * `show-icon.py` - command-line tool to display icon at specific index
 * `write-icon.py` - command-line tool to load an icon into the flash of the LCD Sys Info
 * `show-image.py` - command-line tool to display image at specific index
 * `write-image.py` - command-line tool to load an image into the flash of the LCD Sys Info
 * `testsuite.py` - unit tests for the module

 * `clock.py` - a simple clock display
 * `demo.py` - loops through various pylcdsysinfo functions
 * `imageloop.py` - displays all of the images from flash in sequence
 * `info.py` - prints out LCD Sys Info serial, firmware, storage info etc at the console

## License

This code is distributed under the GPL v3 license, see `LICENSE.txt` for more information.
