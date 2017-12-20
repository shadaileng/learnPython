#!/usr/bin/python3
#-*- coding: utf-8 -*-
'''
	*************************
	* Third party module *
	*************************
	powered by %s
'''

from PIL import Image, ImageFilter, ImageFont, ImageDraw
import random

__author__ = 'Shadaileng'

if __name__ == '__main__':
	im = Image.open('./res/face.png')
	w, h = im.size
	print('origin img size: %s %s' % (w, h))
	im.thumbnail((w//2, h//2))
	print('resize: %s %s' % (im.size))
	im.save('./res/face_.png', 'png')
	im2 = im.filter(ImageFilter.BLUR)
	im2.save('./res/face_blur.png', 'png')
	
	def rndChr():
		return chr(random.randint(65, 90))
	def rndColor(flag):
		if flag == 0:
			return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))
		elif flag == 1:
			return (random.randint(65,255), random.randint(65,255), random.randint(65,255))
	width, height = (60 * 4, 60)
	image = Image.new('RGB', (width, height), (255, 255, 255))
	font = ImageFont.truetype('/usr/share/fonts/TTF/DejaVuSans.ttf', 36)
	draw = ImageDraw.Draw(image)
	for x in range(width):
		for y in range(height):
			draw.point((x, y), fill = rndColor(1))
	for i in range(4):
		draw.text((60 * i + 10, 10), rndChr(), font = font, fill=rndColor(1))
	image = image.filter(ImageFilter.BLUR)
	image.save('./res/code.jpg', 'jpeg')
