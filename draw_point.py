
from luma.core.interface.serial import spi, noop
from luma.led_matrix.device import max7219
from luma.core.render import canvas
from PIL import Image, ImageDraw
from random import randint
import time

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=1)

while True:
	with canvas(device) as draw:
		for i in range(8):
			for j in range(8):
				if randint(0,1)==0:	
					draw.point((i,j), fill="white")
        time.sleep(0.2)


