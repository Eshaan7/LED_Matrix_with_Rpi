#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-18 Richard Hull and contributors
# See LICENSE.rst for details.

import re
import time
import argparse
from HTMLParser import HTMLParser

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

def demo(msg, n, block_orientation, rotate, provided_font):
	# create matrix device
	serial = spi(port=0, device=0, gpio=noop())
	device = max7219(serial, cascaded=n or 1, block_orientation=block_orientation, rotate=rotate or 0)
	print("***Created device***")
	# start demo
	h = HTMLParser()
	l = len(msg)
	for i in range( len(msg) ):
		if msg[i]=='&':
			msg = msg[:i-1] + h.unescape(msg[i::])
			break

	print(msg)
	show_message(device, msg, fill="white", font=proportional(SINCLAIR_FONT), scroll_delay=0.07)
	#time.sleep(2)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='matrix_scroll arguments',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	parser.add_argument('--msg', '-m', type=str, default="fuck off ya bitch", help='Message to be displayed')
	parser.add_argument('--cascaded', '-n', type=int, default=1, help='Number of cascaded MAX7219 LED matrices')
	parser.add_argument('--block-orientation', type=int, default=0, choices=[0, 90, -90], help='Corrects block orientation when wired vertically')
	parser.add_argument('--rotate', type=int, default=0, choices=[0, 1, 2, 3], help='Rotate display 0=0°, 1=90°, 2=180°, 3=270°')
	parser.add_argument('--font', '-f', type=str, default="TINY_FONT", help='Font to display text in')
	args = parser.parse_args()

	try:
		demo(args.msg, args.cascaded, args.block_orientation, args.rotate, args.font)
	except KeyboardInterrupt:
		pass

