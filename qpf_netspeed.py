#!usr/bin/python3
#-*- coding: utf-8 -*-

"""
	******************
	*    NetSpeed    *
	******************
	     Powered By %s
"""

__author__ = 'Shadaileng'

import re, time, cv2 as cv, numpy as np

def getCurrentDownloadRate(adapter='wlp3s0b1'):
	cur_rate = 0
	cur_rate = []
	with open('/proc/net/dev') as f:
		data = f.read()
		pos = data.find('wlp3s0b1:')
#		cur_rate = int(re.search('\d+\s', data[data.find(adapter + ': '):]).group(0))
#		print('current data: %d' % cur_rate)
		dowm_up_rate = re.search('\d+\s+\d+\s', data[data.find(adapter + ': '):]).group(0)
#		print(dowm_up_rate)
		iter_ = re.finditer('\d+', dowm_up_rate)
		for it in iter_:
			cur_rate.append(int(it.group()))
	return cur_rate

def drawText(roi, text, font, scale, thinkness, w, h, style, winName='text'):
	roi[:,:,:] = 0
	for i, txt in enumerate(text):
		textSize = cv.getTextSize(' ', font, scale, thinkness)
		cw, ch = (textSize[0][0], textSize[0][1])
		
		textSize = cv.getTextSize(txt, font, scale, thinkness)
		textw, texth = (textSize[0][0], textSize[0][1])
		x, y = ((w - textw - cw) // 2, (h // 2 - texth) // 2 + texth + (h // 2) * i)
	#	cv.line(roi, (0, y), (w, y), (0, 255, 255), 1)
	#	print('c\tr\tx\ty\tw\th')
	#	print('%s\t%s\t%s\t%s\t%s\t%s' % (w, h, x, y, textSize[0][0], textSize[0][1]))
		cv.putText(roi, txt, (x, y), cv.FONT_HERSHEY_SIMPLEX, scale, (0, 255, 0), thinkness, style)
		
		cx, cy = (textw + x + cw // 2, (h // 2 - texth) // 2 + (h // 2) * i)
		if i == 1:
			points = np.array([[0 + cx, ch + cy], [cw // 2 + cx, 0 + cy], [cw + cx, ch + cy]], np.int32).reshape((-1, 1, 2))
			cv.polylines(roi, [points], True, (0, 255, 255), thinkness, style)
		else:
			points = np.array([[0 + cx, 0 + cy], [cw // 2 + cx, ch + cy], [cw + cx, 0 + cy]], np.int32).reshape((-1, 1, 2))
			cv.polylines(roi, [points], True, (0, 255, 255), thinkness, style)
	cv.imshow('netSpeed', roi)
	key = cv.waitKey(1)
	if key == ord('q'):
		return True

def getNetSpeed():
	rates_tmp = getCurrentDownloadRate()
	fps = 0.8
	frames = 1 / fps
	
	r, c = 60, 140
	buf = ['%s Bytes/s' % (0.0), '%s Bytes/s' % (0.0)]
	font = cv.FONT_HERSHEY_SIMPLEX
	scale = 0.5
	thinkness = 1
	style = cv.LINE_AA
	
	
	roi = np.zeros((r, c, 3), np.uint8)
	
#	textSize = cv.getTextSize(buf, font, scale, thinkness)
	
	cv.imshow('netSpeed', roi)
	timeb = time.time()
	unit = [['', ''], ['', '']]
	while True:
		rates_cur = getCurrentDownloadRate()
#		print('rates_cur: %s, rates_tmp: %s' % (rates_cur, rates_tmp))
		rates_dalte = [rates_cur[0] - rates_tmp[0], rates_cur[1] - rates_tmp[1]]
		rates_tmp = rates_cur
		time_cur = time.time()
#		print('time_cur: %s, timeb: %s' % (time_cur, timeb))
		time_dalta = time.time() - timeb
		timeb = time.time()
		
#		print('%d, %.3f, %.3f, %.3f' % (rates_dalte, rates_dalte / frames, rates_dalte / frames / 1000, rates_dalte / frames / 1000000))
		
		for i, rate in enumerate(rates_dalte):
			if rate / time_dalta >= 1000000:
				unit[i][0] = 'Mb/s'
				unit[i][1] = 1000000
			else:
				unit[i][0] = 'Kb/s'
				unit[i][1] = 1000
	
#		if rates_dalte / time_dalta >= 1000000:
#			unit = 'Mb/s'
#			unit_ = 1000000
#		else:
#			unit = 'Kb/s'
#			unit_ = 1000
			
#		print('frames: %s, time_dalta: %s' % (frames, time_dalta))
		if time_dalta < frames:
			time.sleep(frames - time_dalta)
#			print('frames - time_dalta: %s' % (frames - time_dalta))
		buf[0] = '%.3f %s' % ((rates_dalte[0] / (time_dalta) / unit[0][1], unit[0][0]))
		buf[1] = '%.3f %s' % ((rates_dalte[1] / (time_dalta) / unit[1][1], unit[1][0]))
#		print(buf)
		isExist = drawText(roi, buf, font, scale, thinkness, c, r, style, 'roi')
		if isExist: break
	
if __name__ == '__main__':
	print(__doc__ % __author__)
	
	getNetSpeed()
#	getCurrentDownloadRate()
