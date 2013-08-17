#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MPD client info example (requires python-mpd)
"""

import sys
from mpd import MPDClient, CommandError
from socket import error as SocketError
from time import sleep
from pylcdsysinfo import LCDSysInfo, BackgroundColours, TextColours, TextAlignment, TextLines
from datetime import timedelta

HOST = 'localhost'
PORT = '6600'
PASSWORD = None


def mpd_connect(_host='localhost', _port='6600', _password=None):
	try:
		client = MPDClient()
		client.connect(_host, _port)
		if _password is not None:
			client.password(_password)
		return client
	except CommandError:
		client.disconnect()
	except SocketError:
		pass
	return False


def mpd_song_time(time):
	time = time.split('.', 1)[0]
	time = str(timedelta(seconds=int(time)))
	time = time.split(':')[-2:]
	time = ':'.join(time)
	return time


def lcd_connect():
	lcd = LCDSysInfo()
	lcd.clear_lines(TextLines.ALL, BackgroundColours.BLACK)
	lcd.dim_when_idle(True)
	lcd.set_brightness(255)
	lcd.save_brightness(127, 255)
	lcd.set_text_background_colour(BackgroundColours.BLACK)
	return lcd


def lcd_clear_lines(lcd):
	lcd.clear_lines(TextLines.ALL, BackgroundColours.BLACK)


def lcd_update_song_time(lcd, elapsed):
	lcd.display_text_on_line(5, elapsed, False, TextAlignment.LEFT, TextColours.WHITE)


def lcd_update_current_song(lcd, song):
	lcd.display_text_on_line(1, '', False, TextAlignment.LEFT, TextColours.WHITE)
	lcd.display_text_on_line(2, song['title'], False, TextAlignment.LEFT, TextColours.WHITE)
	lcd.display_text_on_line(3, song['artist'], False, TextAlignment.LEFT, TextColours.WHITE)
	lcd.display_text_on_line(4, song['album'], False, TextAlignment.LEFT, TextColours.WHITE)
	lcd.display_text_on_line(5, '0:01', False, TextAlignment.LEFT, TextColours.WHITE)
	lcd.display_text_on_line(6, '', False, TextAlignment.LEFT, TextColours.WHITE)


def main():
	lcd = lcd_connect()

	mpd = mpd_connect(HOST, PORT, PASSWORD)
	if mpd is not False:
		last = None
		while(1):
			status = mpd.status()
			song = mpd.currentsong()

			if 'title' in song:
				if last != song:
					lcd_update_current_song(lcd, song)

				if 'elapsed' in status:
					elapsed = mpd_song_time(status['elapsed'])
					lcd_update_song_time(lcd, elapsed)

			else:
				lcd_clear_lines(lcd)
			last = song

			sleep(1)

		mpd.disconnect()
	else:
		print("Failed to connect")
		sys.exit(1)


if __name__ == "__main__":
	main()


