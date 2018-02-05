#!usr/bin/python3
#-*- coding: utf-8 -*-

'''
	******************
	*       App      *
	******************
	     Powered By %s
'''

__author__ = 'Shadaileng'

import cv2 as cv, matplotlib.pyplot as plt

def rws():
	img = cv.imread('./res/face.png', 1)

	print('shape: %s' % str(img.shape))
	print('size: %s' % img.size)
	print('dtype: %s' % img.dtype)

	width, height = img.shape[:2]

	cv.putText(img, 'Demo', (width//2, height // 2), 0, 0.5, (0,0,255),2)

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
	if not cap.isOpened():
		print('open')
		cap.open()
	for i in range(1, 19):
		print(cap.get(i))
	while True:
		ret, frame = cap.read()
		gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
		cv.imshow('frame', gray)
		if cv.waitKey(1) == ord('q'):
			break
	cap.release()
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


if __name__ == '__main__':
	print(__doc__ % __author__)
#	rws()
#	rws2()
#	camera_()
	video_()
