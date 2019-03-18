#!usr/bin/python3
#-*- coding: utf-8 -*-

"""
	******************
	*      OpenCV    *
	******************
	     Powered By %s
"""

__author__ = 'Shadaileng'

import functools, cv2 as cv, numpy as np, matplotlib.pyplot as plt

def load_img(path):
	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args, **kw):
			b = cv.getTickCount()
			if path:
				src = cv.imread(path, cv.IMREAD_UNCHANGED)
				cv.namedWindow('Origin', cv.WINDOW_NORMAL)
				cv.imshow('Origin', src)
			func(*args, **kw)
			
			e = cv.getTickCount()
			
			ms = (e - b)/cv.getTickFrequency() * 1000
			print('last: %f ms' % ms)
			cv.waitKey(0)
			cv.destroyAllWindows()
			return 1
		wrapper.__path__ = path
		return wrapper
	return decorator

def get_min_rc(src1, src2):
	return (min(src1.shape[0], src2.shape[0]), min(src1.shape[1], src2.shape[1]))

@load_img('./res/tumblr.jpg')
def test(a = 1, b=2):
	print('test', a, b, test.__path__)
#	cv.imshow('src', test.__src__)

def main():
	src = cv.imread('./res/tumblr.jpg', cv.IMREAD_UNCHANGED)
	src1 = cv.imread('./res/tumblr.png', cv.IMREAD_UNCHANGED)
	cv.namedWindow('Origin', cv.WINDOW_NORMAL)
	cv.imshow('Origin', src)
	cv.namedWindow('Origin1', cv.WINDOW_NORMAL)
	cv.imshow('Origin1', src)


	cv.waitKey(0)
	cv.destroyAllWindows()

@load_img('./res/tumblr.jpg')
def fill_color():
	src = cv.imread(fill_color.__path__, cv.IMREAD_UNCHANGED)
	r, c = src.shape[:2]
	mask = np.zeros((r + 2, c + 2), np.uint8)
	cv.floodFill(src, mask, (100, 100), (0, 255, 255), (100, 100, 100), (50, 50, 50), cv.FLOODFILL_FIXED_RANGE)
	cv.namedWindow('fill_color', cv.WINDOW_NORMAL)
	cv.imshow('fill_color', src)

@load_img(None)
def fill_binary():
	r, c = 400, 400
	src = np.zeros((r, c, 3), np.uint8)
	src[100:300, 100:300] = 255
	# cv.namedWindow('origin', cv.WINDOW_NORMAL)
	cv.imshow('origin', src)
	mask = np.ones((r + 2, c + 2), np.uint8)
	mask[150:250, 150:250] = 0
	cv.floodFill(src, mask, (200, 200), (0, 255, 255), cv.FLOODFILL_MASK_ONLY)
	# cv.namedWindow('fill_color', cv.WINDOW_NORMAL)
	cv.imshow('fill_color', src)

@load_img(None)
def blur():
	ks = 299
	# a = np.arange(1, ks**2 + 1).reshape((ks , ks)) % 255
	a = cv.imread('./res/tumblr.png', cv.IMREAD_UNCHANGED)
	print(a.shape)
	# print(a)
	# a_ = cv.blur(a, (3,3))
	# a_ = cv.GaussianBlur(a, (3, 3), 0)
	a_ = cv.bilateralFilter(cv.cvtColor(a, cv.COLOR_BGR2GRAY), 1, 100, 75)
	# kernel = np.ones((3, 3), np.float32) / 9
	# a_ = cv.filter2D(a, -1, kernel)
	cv.imshow('1', a)
	cv.imshow('2', a_)
	cv.waitKey(0)
	cv.destroyAllWindows()
	# print(a_)

@load_img('./res/tumblr.jpg')
def histogram():
	src = cv.imread(histogram.__path__, cv.IMREAD_UNCHANGED)
	bins = 256
	plt.hist(src.ravel(), bins, [0, bins], histtype='barstacked')
	# plt.hist([1, 3, 3, 5, 5, 8], bins, [0, bins], histtype='stepfilled', orientation='vertical', align='left', stacked=True)
	chanels = ['blue', 'green', 'red']
	for i, c in enumerate(chanels):
		hist = cv.calcHist([src], [i], None, [256], [0, 256])
		plt.plot(hist, color=c)
	hist, bins_ = np.histogram(src.ravel(), 256, [0, 256])
	# print(bins_)
	plt.plot(hist, color='gray')
	hist = np.bincount(src.ravel(), minlength=256)
	plt.plot(hist, color='orange')
	if bins <= 20: plt.xticks(range(bins))
	plt.show()

@load_img('./res/tumblr.png')
def equalize():
	src = cv.imread(equalize.__path__, cv.IMREAD_UNCHANGED)
	gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
	equalize_ = cv.equalizeHist(gray)
	clahe = cv.createCLAHE(clipLimit=5.0, tileGridSize=(8, 8))
	clahe_ = clahe.apply(gray)
	hist = np.bincount(gray.ravel(), minlength=256)
	plt.plot(hist, color='red')

	hist = np.bincount(equalize_.ravel(), minlength=256)
	plt.plot(hist, color='green')

	hist = np.bincount(clahe_.ravel(), minlength=256)
	plt.plot(hist, color='blue')

	cv.imshow('gray', gray)
	cv.imshow('equalizeHist', equalize_)
	cv.imshow('clahe', clahe_)
	plt.show()

@load_img('./res/tumblr.png')
def histogram_plt():
	src = cv.imread(histogram_plt.__path__, cv.IMREAD_UNCHANGED)
	plt.subplot(221)
	plt.hist(src[:,:,0].ravel(), 256, [0, 256], color='blue', histtype='step')
	plt.hist(src[:,:,1].ravel(), 256, [0, 256], color='green', histtype='step')
	plt.hist(src[:,:,2].ravel(), 256, [0, 256], color='red', histtype='step')

	plt.subplot(222)
	hist, bins = np.histogram(src[:,:,0].ravel(), 256, [0, 256])
	plt.plot(hist, color='b')
	hist, bins = np.histogram(src[:,:,1].ravel(), 256, [0, 256])
	plt.plot(hist, color='g')
	hist, bins = np.histogram(src[:,:,2].ravel(), 256, [0, 256])
	plt.plot(hist, color='r')

	plt.subplot(223)
	hist = np.bincount(src[:,:,0].ravel(), minlength=256)
	plt.plot(hist, color='b')
	hist = np.bincount(src[:,:,1].ravel(), minlength=256)
	plt.plot(hist, color='g')
	hist = np.bincount(src[:,:,2].ravel(), minlength=256)
	plt.plot(hist, color='r')

	plt.subplot(224)
	hist = cv.calcHist([src], [0], None, [256], [0, 256])
	plt.plot(hist, 'b')
	hist = cv.calcHist([src], [1], None, [256], [0, 256])
	plt.plot(hist, 'g')
	hist = cv.calcHist([src], [2], None, [256], [0, 256])
	plt.plot(hist, 'r')

	plt.show()

@load_img('./res/tumblr.png')
def histogram_cv2():
	src = cv.imread(histogram_cv2.__path__, cv.IMREAD_UNCHANGED)
	output = None
	for i, c in enumerate([(255, 0, 0), (0, 255, 0), (0, 0, 255)]):
		hist = cv.calcHist([src], [i], None, [256], [0, 256])
		data = hist.ravel()
		cdf = np.cumsum(data)
		cdf_normalize = cdf / max(cdf) * max(data)
		output = drawData(cdf_normalize, output, 256, (512, 512), c, (0.05, 0.95, 0.05, 0.95), histtype='line')
		output = drawData(data, output, 256, (512, 512), c, (0.05, 0.95, 0.05, 0.95), histtype='line')

	cv.imshow('histogram', output)
def drawData(data, output, BINs=256, rc=(256, 256), color = (255, 255, 255), padding=(0, 1, 0, 1), histtype='hist', isShow=False):
	r, c = rc
	if output is None:
		output = np.zeros((r, c, 3), np.uint8)
	else:
		r, c = output.shape[:2]
	top = int((padding[0]) * r)
	bottom = int((padding[1]) * r)
	left = int((padding[2]) * r)
	right = int((padding[3]) * r)
	BIN = int(256 / BINs)
	cv.line(output, (left, 0), (left, r), (255, 0, 255))
	cv.line(output, (0, bottom), (c, bottom), (255, 0, 255))

	data = data.reshape((BINs, BIN)).sum(axis=1)

	data = np.floor(data / max(data) * (bottom - top))

	for i in range(BINs):
		x, y = (int(i / BINs * (right - left) + left), int(bottom - data[i]))
		x_, y_ = (int((i + 1) / BINs * (right - left) + left), int(bottom - data[i + 1])) if i < (BINs - 1) else (int((i + 1) / BINs * (right - left) + left), (bottom - 1))
		if histtype == 'hist':
			cv.line(output, (x, y), (x, int(bottom - 1)), color)
			cv.line(output, (x, y), (x_, y), color)
			cv.line(output, (x_, y), (x_, y_), color)
		elif histtype == 'line':
			if i < BINs - 1:
				cv.line(output, (x, y), (x_, y_), color)
	if isShow:
		cv.imshow('histogram', output)
	return output

@load_img('./res/tumblr_.png')
def draw2DHist():
	src = cv.imread(draw2DHist.__path__, cv.IMREAD_UNCHANGED)
	hsv = cv.cvtColor(src[100:200, 100:200], cv.COLOR_BGR2HSV)
	
	hsv_map = np.zeros((180, 256, 3), np.uint8)
	h, s = np.indices(hsv_map.shape[:2])
	hsv_map[:,:,0] = h
	hsv_map[:,:,1] = s
	hsv_map[:,:,2] = 255
	
	cv.imshow('hsv_map_BGR_HSV', np.hstack((cv.cvtColor(hsv_map, cv.COLOR_HSV2BGR), hsv_map)))
	
	dark = hsv[:,:,2] < 32
	hsv[dark] = 0
	
#	h = hsv[:,:,0]
#	s = hsv[:,:,1]

#	hist, xbins, ybins = np.histogram2d(h.ravel(), s.ravel(), [180, 256], [[0, 180], [0, 256]])
	
#	print(xbins, ybins)
	
	hist = cv.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])
	
	np.clip(hist * 0.005 * 10, 0, 1)

	vis = hsv_map * hist[:,:,np.newaxis] / 255.0

	cv.imshow('hist', vis)
	
#	plt.imshow(hist, interpolation='nearest')
#	plt.show()
	
	
	
	'''
	print(hist.shape)
	
	r, c = src.shape[:2]
	output = np.zeros((r, c, 3), np.uint8)
	data = hist.ravel()
	max_ = max(data)
	data_ = data / max_ * 0.9 * r
	color = (255, 255, 0)
	
	output = drawData(data_, output, color, (0.05, 0.95, 0.05, 0.95))
	
	cv.imshow('2D', np.hstack((hsv, output)))
	'''

def draw2DHist_vedio():
	
	hsv_map = np.zeros((180, 256, 3), np.uint8)
	h, s = np.indices(hsv_map.shape[:2])
	hsv_map[:,:,0] = h
	hsv_map[:,:,1] = s
	hsv_map[:,:,2] = 255
	
	cv.imshow('hsv_map_BGR_HSV', np.hstack((cv.cvtColor(hsv_map, cv.COLOR_HSV2BGR), hsv_map)))
	
	capture = cv.VideoCapture(0)
	if not capture.isOpened():
		capture.open()
	
	while True:
		ret, fram = capture.read()
		if ret:
			src = fram
			cv.imshow('frame', src)
			hsv = cv.cvtColor(src, cv.COLOR_BGR2HSV)
			
			dark = hsv[:,:,2] < 32
			hsv[dark] = 0
			
			hist = cv.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])
			
			np.clip(hist * 0.005 * 10, 0, 1)

			vis = hsv_map * hist[:,:,np.newaxis] / 255.0

			cv.imshow('hist', vis)
			key = cv.waitKey(25)
			if key == ord('q'):
				break
		else:
			break
	capture.release()

@load_img('./res/tumblr.png')
def histProject():
	src = cv.imread(histProject.__path__, cv.IMREAD_UNCHANGED)
	r, c, h, w = [100, 110, 20, 25]
	roi = src[r:r+h, c:c+w]
	cv.imshow('roi', roi)
	src_hsv = cv.cvtColor(src, cv.COLOR_BGR2HSV)
	roi_hsv = cv.cvtColor(roi, cv.COLOR_BGR2HSV)

	I = cv.calcHist([roi_hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])
	cv.normalize(I, I, 0, 255, cv.NORM_MINMAX)

	dst = cv.calcBackProject([src_hsv], [0, 1], I, [0, 180, 0, 256], 1)

	disc = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
	dst = cv.filter2D(dst, -1, disc)

	ret,thresh = cv.threshold(dst,50,255,0)

	thresh = cv.merge((thresh, thresh, thresh))
	res = cv.bitwise_and(src, thresh)

	cv.imshow('res', np.hstack((src, thresh, res)))

@load_img('./res/tumblr.png')
def npBackProject():
	src = cv.imread(npBackProject.__path__, cv.IMREAD_UNCHANGED)
	r, c, h, w = [100, 110, 20, 25]
	roi = src[r:r+h, c:c+w]
	cv.imshow('roi', roi)

	src_hsv = cv.cvtColor(src, cv.COLOR_BGR2HSV)
	roi_hsv = cv.cvtColor(roi, cv.COLOR_BGR2HSV)

	M = cv.calcHist([src_hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])
	I = cv.calcHist([roi_hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])

	M = np.ma.masked_equal(M, 0)
	R = I / M
	R = np.ma.filled(R, 0).astype('float32')
	h = src_hsv[:,:,0]
	s = src_hsv[:,:,1]

	B = R[h.ravel(), s.ravel()]
	B = np.minimum(B, 1)

	B = B.reshape(src_hsv.shape[:2])
	disc = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
	cv.filter2D(B, -1, disc)
	B = np.uint8(B * 100)
	print(np.max(B))
	cv.normalize(B, B, 0, 255, cv.NORM_MINMAX)

	ret, thresh = cv.threshold(B, 50, 255, 0)
	thresh = cv.merge((thresh, thresh, thresh))
	res = cv.bitwise_and(src, thresh)

	cv.imshow('res', np.hstack((src, thresh, res)))
	

if __name__ == '__main__':
	print(__doc__ % __author__)
#	test()
#	main()
#	fill_color()
#	fill_binary()
#	blur()
#	histogram()
#	equalize()
#	drawHist_()
#	draw2DHist()
#	draw2DHist_vedio()
	histProject()
#	npBackProject()
