#!usr/bin/python3
#-*- coding: utf-8 -*-

'''
	******************
	*      OpenCV    *
	******************
	     Powered By %s
'''

__author__ = 'Shadaileng'

import cv2 as cv, matplotlib.pyplot as plt, numpy as np, matplotlib.gridspec as gridspec

def rws():
	img = cv.imread('./res/face.png', 1)

	print('shape: %s' % str(img.shape))
	print('size: %s' % img.size)
	print('dtype: %s' % img.dtype)

	width, height = img.shape[:2]

	cv.putText(img, 'Demo', (width//2, height // 2), 0, 0.5, (0,0,255),2)

	print(img.item(10, 10, 2))
	row, col = (140, 70)
	row1, col1 = (80, 170)
	eye = img[row:row+100, col:col+100]
	img[row1:row1+100, col1:col1+100] = eye

#	r, g, b = cv.split(img)
#	g = g + 100
#	img = cv.merge((r, g, b))
	
	r = img[:,:,0]
	g = img[:,:,1]
	b = img[:,:,2]

	img[:,:,1] = img[:,:,1] + 100

#	for x in range(100, 200):
#		for y in range(100, 200):
#			pass
#			img[x,y] = 255
#			img.itemset((x, y, 1), 255)
#			img.itemset((x, y, 2), 0)
#			img.itemset((x, y, 0), 255)

#	cv.namedWindow('face', cv.WINDOW_AUTOSIZE)
	cv.namedWindow('face', cv.WINDOW_NORMAL)
	cv.imshow('face', img)

	k = cv.waitKey(0)
	if k == 27:
		cv.destroyAllWindows()
	elif k == ord('s'):
		cv.imwrite('./res/tmp.png', img)
		cv.destroyAllWindows()

def rws2():
	img = cv.imread('./res/face.png', cv.IMREAD_COLOR)
	fig = plt.figure()
	plt.subplot(1, 2, 1)
	plt.imshow(img, cmap=None, interpolation='nearest')
	plt.xticks(())
	plt.yticks(())

	plt.subplot(1, 2, 2)
	img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	plt.imshow(img, cmap='gray', interpolation='bicubic')
	plt.xticks(())
	plt.yticks(())
	plt.show()

def camera_():
	cap = cv.VideoCapture(1)
	fourcc = cv.VideoWriter_fourcc(*'XVID')
	out = cv.VideoWriter('./res/out.avi', fourcc, 25, (640, 480))
	if not cap.isOpened():
		print('open')
		cap.open()
	for i in range(1, 19):
		print(cap.get(i))
	while True:
		ret, frame = cap.read()
		if ret:
			gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
			out.write(frame)
			cv.imshow('frame', gray)
			if cv.waitKey(25) == ord('q'):
				break
		else:
			break
	cap.release()
	out.release()
	cv.destroyAllWindows()


def video_():
	cap = cv.VideoCapture('./res/a.mp4')
	if not cap.isOpened():
		print('open')
		cap.open()
	for i in range(1, 19):
		print(cap.get(i))
	while True:
		ret, frame = cap.read()
		gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
		cv.imshow('frame', gray)
		if cv.waitKey(25) == ord('q'):
			break
	cap.release()
	cv.destroyAllWindows()

def video_save():
	cap = cv.VideoCapture('./res/a.mp4')
	fourcc = cv.VideoWriter_fourcc(*'XVID')
	out = cv.VideoWriter('./res/out.avi', fourcc, 25, (640, 480))
	if not cap.isOpened():
		print('open')
		cap.open()
	for i in range(1, 19):
		print(cap.get(i))
	while True:
		ret, frame = cap.read()
		if ret:
			gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
			out.write(frame)
			cv.imshow('frame', gray)
			if cv.waitKey(25) == ord('q'):
				break
		else:
			break
	cap.release()
	out.release()
	cv.destroyAllWindows()

img = np.zeros((512, 512, 3), np.uint8)

def draw():
	cv.line(img, (10, 10), (256, 256), (255, 0, 0), 5, cv.LINE_AA)
	cv.rectangle(img, (10, 10), (256, 256), (0, 255, 0), 5, cv.LINE_AA)
	cv.circle(img, (133, 133), 123, (0, 0, 255), 5, cv.LINE_AA)
	cv.ellipse(img, (133, 133), (123, 62), 45, 0, 360, (0, 255, 255), 5, cv.LINE_AA)

	points = np.array([[256, 256], [502, 256], [502, 502], [256, 502]], np.int32)
	points = points.reshape((-1, 1, 2))
	cv.polylines(img, [points], True, (255, 255, 255), 5, cv.LINE_AA)

	font = cv.FONT_HERSHEY_SIMPLEX
	cv.putText(img, 'OpenCV', (260, 384), font, 2, (128, 256, 128), 5, cv.LINE_AA)

	cv.namedWindow('Draw', cv.WINDOW_NORMAL)
	cv.imshow('Draw', img)

	k = cv.waitKey(0)
	if k == ord('q'):
		cv.destroyAllWindows()

drawing = False
mod = True
ix, iy = (-1, -1)
def drawcircle(event, x, y, flags, param):
	global drawing, mod, ix, iy
	if event == cv.EVENT_LBUTTONDOWN:
		drawing = True
		ix, iy = (x, y)
	elif event == cv.EVENT_MOUSEMOVE and cv.EVENT_FLAG_LBUTTON:
		if drawing:
			if mod:
				cv.rectangle(img, (ix, iy), (x, y), (255, 0, 255), -1, cv.LINE_AA)
			else:
				cv.circle(img, (x,y), 3, (255, 255, 0), -1, cv.LINE_AA)
	elif event == cv.EVENT_LBUTTONUP:
		drawing = False
		


def mouse_events():
#	events = [i for i in dir(cv) if 'EVENT' in i]
#	print(events)
	global mod
	cv.namedWindow('Mouse_Event')
	cv.setMouseCallback('Mouse_Event', drawcircle)

	while True:
		cv.imshow('Mouse_Event', img)
		k = cv.waitKey(1)
		if k == ord('q'):
			break
		elif k == ord('m'):
			mod = not mod

	cv.destroyAllWindows()

def nothing(x):
	print('x: %s' % x)
def trackbar():
	cv.namedWindow('TrackBar')
	cv.createTrackbar('R', 'TrackBar', 100, 255, nothing)
	cv.createTrackbar('G', 'TrackBar', 0, 255, nothing)
	cv.createTrackbar('B', 'TrackBar', 0, 255, nothing)
	switch = '0:OFF 1:ON'
	cv.createTrackbar(switch, 'TrackBar', 0, 1, nothing)

	while True:
		cv.imshow('TrackBar', img)
		k = cv.waitKey(1)
		if k == ord('q'):
			break
		r = cv.getTrackbarPos('R', 'TrackBar')
		g = cv.getTrackbarPos('G', 'TrackBar')
		b = cv.getTrackbarPos('B', 'TrackBar')
		s = cv.getTrackbarPos(switch, 'TrackBar')
		if s:
			img[:] = [r,g,b]
		else:
			img[:] = 0
	cv.destroyAllWindows()

def makeborder():
	img = cv.imread('./res/tumblr.png', cv.IMREAD_COLOR)
	fig = plt.figure()
	plt.subplot(231)
	plt.imshow(img, 'gray')
	plt.xticks(())
	plt.yticks(())

	plt.subplot(232)
	plt.imshow(cv.copyMakeBorder(img, 100, 100, 100, 100, cv.BORDER_CONSTANT, value=(255, 0, 0)))
	plt.xticks(())
	plt.yticks(())

	plt.subplot(233)
	plt.imshow(cv.copyMakeBorder(img, 100, 100, 100, 100, cv.BORDER_REFLECT))
	plt.xticks(())
	plt.yticks(())

	plt.subplot(234)
	plt.imshow(cv.copyMakeBorder(img, 100, 100, 100, 100, cv.BORDER_DEFAULT))
	plt.xticks(())
	plt.yticks(())

	plt.subplot(235)
	plt.imshow(cv.copyMakeBorder(img, 100, 100, 100, 100, cv.BORDER_REPLICATE))
	plt.xticks(())
	plt.yticks(())

	plt.subplot(236)
	plt.imshow(cv.copyMakeBorder(img, 100, 100, 100, 100, cv.BORDER_WRAP))
	plt.xticks(())
	plt.yticks(())

	plt.show()


def operate():
	img1 = cv.imread('./res/tumblr.png', cv.IMREAD_COLOR)
	img2 = cv.imread('./res/face.png', cv.IMREAD_COLOR)
	fig = plt.figure()
	plt.subplot(331)
	plt.imshow(img1, 'gray')
	plt.xticks(())
	plt.yticks(())

	plt.subplot(332)
	plt.imshow(img2, 'gray')
	plt.xticks(())
	plt.yticks(())

	plt.subplot(333)
	plt.imshow(img1[0:512, 0:512] + img2)
	plt.xticks(())
	plt.yticks(())

	plt.subplot(334)
	plt.imshow(cv.add(img1[0:512, 0:512], img2))
	plt.xticks(())
	plt.yticks(())

	plt.subplot(335)
	plt.imshow(cv.addWeighted(img1[0:512, 0:512], 0.7, img2, 0.3, 1))
	plt.xticks(())
	plt.yticks(())

	plt.show()

def bitwise():
	img1 = cv.imread('./res/tumblr.png', cv.IMREAD_COLOR)
	img2 = cv.imread('./res/face.png', cv.IMREAD_COLOR)

	fig = plt.figure()
	gs = gridspec.GridSpec(3, 3)

	plt.subplot(gs[0,0])
	plt.imshow(img1)
	plt.xticks(())
	plt.yticks(())

	plt.subplot(gs[0,1])
	plt.imshow(img2)
	plt.xticks(())
	plt.yticks(())

	h, w = (img1.shape[0] if img1.shape[0] < img2.shape[0] else img2.shape[0], img1.shape[1] if img1.shape[1] < img2.shape[1] else img2.shape[1])
	ret, mask = cv.threshold(cv.cvtColor(img2[0:h,0:w], cv.COLOR_BGR2GRAY), 170, 255, cv.THRESH_BINARY)
	mask_ink = cv.bitwise_not(mask)
	r, c = (0, 0)
	bg = cv.bitwise_and(img1[r:r + h, c:c + w], img1[r:r + h, c:c + w], mask=mask)
	fg = cv.bitwise_and(img1[r:r + h, c:c + w], img1[r:r + h, c:c + w], mask=mask_ink)
	img1[r:r + h, c:c + w] = cv.add(bg, fg)

	plt.subplot(gs[1,0])
	plt.imshow(mask)
	plt.xticks(())
	plt.yticks(())
	
	plt.subplot(gs[1,1])
	plt.imshow(mask_ink)
	plt.xticks(())
	plt.yticks(())
	
	plt.subplot(gs[2,0])
	plt.imshow(bg)
	plt.xticks(())
	plt.yticks(())
	
	plt.subplot(gs[2,1])
	plt.imshow(fg)
	plt.xticks(())
	plt.yticks(())
	
	plt.subplot(gs[:2,2])
	plt.imshow(img1)
	plt.xticks(())
	plt.yticks(())

	plt.subplot(gs[2,2])
	plt.imshow(cv.add(bg, fg))
	plt.xticks(())
	plt.yticks(())

	plt.show()

def catch_white():
	capture = cv.VideoCapture(1)
	if not capture.isOpened():
		print('open capture')
		capture.open()
	while True:
		ret, frame = capture.read()
		if ret:
			catch_color(frame, np.array([0, 0, 221]), np.array([180, 30, 255]))
			k = cv.waitKey(1)
			if k == ord('q'):
				break
		else:
			break
	cv.destroyAllWindows()

def catch_color(frame, lower, upper):
	hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
	mask = cv.inRange(hsv, lower, upper)
	res = cv.bitwise_and(frame, frame, mask=mask)
	cv.imshow('frame', frame)
	cv.imshow('hsv', hsv)
	cv.imshow('mask', mask)
	cv.imshow('res', res)

def trans_geometry():
	img = cv.imread('./res/tumblr.png', cv.IMREAD_COLOR)

	h, w = img.shape[:2]

	cv.imshow('img', img)
	cv.imshow('scale:0.5', cv.resize(img, None, fx=0.5, fy=0.5, interpolation=cv.INTER_CUBIC))
	cv.imshow('scale:2', cv.resize(img, (w*2, h*2), interpolation=cv.INTER_CUBIC))

	cv.waitKey(0)
	cv.destroyAllWindows()

if __name__ == '__main__':
	print(__doc__ % __author__)
#	rws()
#	rws2()
#	camera_()
#	video_()
#	video_save()
#	draw()
#	mouse_events()
#	trackbar()
#	makeborder()
#	operate()
#	bitwise()
#	catch_white()
	trans_geometry()	
