#!/usr/bin/python3
#-*- coding: utf-8 -*-
'''
	***********
	*  Image  *
	***********
	   --powered by %s

'''

__author__ = 'Shadaileng'

from PIL import Image, ImageFilter, ImageFont, ImageDraw
from com.qpf.qpf_log import log_time, log_time_data
import random
def handlefilePath(path):
	filepath = path[:path.rfind('/') + 1]
	name = path[path.rfind('/') + 1:path.rfind('.')] 
	suffix = path[path.rfind('.'):]
	return (filepath, name, suffix)

def blurImg(fileName):
	
	filepath, name, suffix = handlefilePath(fileName)
	im = Image.open(fileName)
	
	log_time_data('open img: %s' % fileName)

	im = im.filter(ImageFilter.BLUR)
	
	log_time_data('img blur')

	fileName_ = filepath + name + '_' + suffix
	
	im.save(fileName_, 'png')
	log_time_data('save img: %s' % fileName_)
	
def generate_code(len):
	code = ''
	for i in range(len):
		t = random.randint(1, 3)
		if t == 1:
			t = random.randint(48, 57)
		elif t == 2:
			t = random.randint(65, 90)
		elif t == 3:
			t = random.randint(97, 122)
		code += chr(t)
	return code
def generate_verifi_code(code, path, height = 60):
	
	width = height * len(code)
	
	font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', int(height * 0.6))
	img = Image.new('RGB', (width, height), (255, 255, 255))
	draw = ImageDraw.Draw(img)
	
	def rndColor(beg, end):
		return (random.randint(beg, end), random.randint(beg, end), random.randint(beg, end))
	
	for x in range(width):
		for y in range(height):
			draw.point((x, y), fill=rndColor(64, 255))
	
	for i, v in enumerate(code):
		draw.text((60 * i + height * 0.3, height * 0.16), v, font = font, fill=rndColor(32, 126))
	
	img = img.filter(ImageFilter.BLUR)
	img.save(path, path[path.rfind('.') + 1:])

if __name__ == '__main__':
	print(__doc__ % __author__)
	
	#blurImg('./res/tumblr.png')
	
	generate_verifi_code(generate_code(5), './res/code.png')
	
