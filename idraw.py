#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-18 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Display the Raspberry Pi logo (loads image as .png).
"""
import re
import time
import argparse
import os.path

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.legacy import text, show_message
from PIL import Image
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, LCD_FONT, SINCLAIR_FONT

def demo(msg, n, block_orientation, rotate, provided_font):
	# create matrix device
	serial = spi(port=0, device=0, gpio=noop())
	device = max7219(serial, cascaded=n or 1, block_orientation=block_orientation, rotate=rotate or 0)
	print("***Created device***")
	# start demo
	print(msg)
	show_message(device, msg, fill="white", font=proportional(SINCLAIR_FONT), scroll_delay=0.1)
	img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
        'images', 'pi_logo.png'))
	logo = Image.open(img_path).convert("RGBA")
	#logo = Image.open(img_path)
	#fff = Image.new(logo.mode, logo.size, (255,) * 4)
	bg = Image.new("RGBA", device.size, "white")
	print("2nd try")
	img = logo.resize((16,8))
	posn = ((device.width - img.width) // 2, -1)
	bg.paste(img, posn)
	#fff.paste(img, posn)
	#device.display(fff.convert(device.mode))
	device.display(bg.convert(device.mode))
	time.sleep(5)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='matrix_scroll arguments',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('--msg', '-m', type=str, default="fuck off ya bitch", help='Message to be displayed')
	parser.add_argument('--cascaded', '-n', type=int, default=1, help='Number of cascaded MAX7219 LED matrices')
	parser.add_argument('--block-orientation', type=int, default=0, choices=[0, 90, -90], help='Corrects blockorient when wired vertically')
	parser.add_argument('--rotate', type=int, default=0, choices=[0, 1, 2, 3], help='Rotate display 0=0°, 1=90°, 2=180°, 3=270°')
	parser.add_argument('--font', '-f', type=str, default="TINY_FONT", help='Font to display text in')
	args = parser.parse_args()

	try:
		demo(args.msg, args.cascaded, args.block_orientation, args.rotate, args.font)
	except KeyboardInterrupt:
		pass

