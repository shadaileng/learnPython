#!/usr/bin/python3
#-*- coding: utf-8 -*-
'''
	**********
	*  Data  *
	**********
	   --powered by %s

'''
__author__ = 'Shadaileng'

import numpy as np, pandas as pd, matplotlib.pyplot as plt

df1 = pd.DataFrame(np.ones((3,4)), columns=['A', 'B', 'C', 'D'], index=[1, 2, 3])
df2 = pd.DataFrame(np.ones((3,4)) * 2, columns=['A', 'B', 'C', 'E'], index=[1, 2, 4])


def axis():
#	df = pd.concat([df1, df2], axis=0)
	df = pd.concat([df1, df2], axis=1)
	print(df)

def ignore():
#	df = pd.concat([df1, df2], axis=0, ignore_index=True)
	df = pd.concat([df1, df2], axis=1, ignore_index=True)
	print(df)
	
def join():
	df = pd.concat([df1, df2], axis=1, ignore_index=True, join='outer')
#	df = pd.concat([df1, df2], axis=1, ignore_index=True,join='inner')
	print(df)

def join_axes():
#	df = pd.concat([df1, df2], axis=1, ignore_index=True, join_axes=[df1.index])
	df = pd.concat([df1, df2], axis=0, ignore_index=True, join_axes=[df1.columns])
	print(df)
	
def append():
	df = df1.append(df2, ignore_index=True)
#	df = pd.concat([df1, df2], axis=0, ignore_index=True, join_axes=[df1.columns])
	print(df)

def merge1():
	left = pd.DataFrame({
		'key1':['K0', 'K1', 'K2', 'K3'],
		'A':['A0', 'A1', 'A2', 'A3'],
		'B':['B0', 'B1', 'B2', 'B3']
	})

	right = pd.DataFrame({
		'key1':['K0', 'K1', 'K2', 'K3'],
		'C':['C0', 'C1', 'C2', 'C3'],
		'D':['D0', 'D1', 'D2', 'D3']
	})
	print(left)
	print(right)
	df = pd.merge(left, right, on='key1')
	print(df)

def merge2():
	left = pd.DataFrame({
		'key1':['K0', 'K1', 'K1', 'K0'],
		'key2':['K0', 'K0', 'K1', 'K1'],
		'A':['A0', 'A1', 'A2', 'A3'],
		'B':['B0', 'B1', 'B2', 'B3']
	})

	right = pd.DataFrame({
		'key1':['K0', 'K1', 'K1', 'K0'],
		'key2':['K0', 'K0', 'K1', 'K2'],
		'C':['C0', 'C1', 'C2', 'C3'],
		'D':['D0', 'D1', 'D2', 'D3']
	})
	print(left)
	print(right)
#	df = pd.merge(left, right, on=['key1', 'key2'], how='inner')
#	df = pd.merge(left, right, on=['key1', 'key2'], how='outer')
	df = pd.merge(left, right, on=['key1', 'key2'], how='inner', indicator=True)
	print(df)

def plot():
	x = np.linspace(-3.14, 3.14, 50)
	y1 = np.sin(x)
	y2 = x* 2
	plt.figure(num=3, figsize=(6, 6))
	plt.xlim(-4, 4)
#	plt.yticks([-1, -0.5, 0.0, 0.5, 1.0], [r'$a$', r'$b$', r'$c$', r'$d$', r'$e$'])
	plt.yticks(np.linspace(-4, 4, 9))
	ax = plt.gca()
	ax.spines['right'].set_color('none')
	ax.spines['top'].set_color('none')
	ax.spines['bottom'].set_position(('data', 0))
	ax.spines['left'].set_position(('data', 0))
	ax.xaxis.set_ticks_position('bottom')
	ax.yaxis.set_ticks_position('left')
	
	for label in ax.get_xticklabels() + ax.get_yticklabels():
		label.set_fontsize(12)
		label.set_bbox(dict(facecolor='white', edgecolor='none', alpha=0.7, zorder=2))
	
	plt.plot(x, y1, label='line')
	plt.plot(x, y2, color='red', linewidth=1.0, linestyle='--', label='sin')
	plt.legend(loc='best')
	
	x0 = 1
	y0 = x0 *2
	plt.plot([x0, x0,], [0, y0,], 'k--', linewidth=2.5)
	plt.scatter([x0,], [y0,], s=50, color='b')

	plt.annotate(r'$x * 2 = %s$' % y0, xy=(x0, y0), xycoords='data', xytext=(+30, -30), textcoords='offset points', fontsize=16, arrowprops=dict(arrowstyle='->', connectionstyle='arc3, rad=.2'))	
	plt.text(-3, 2, r'$plot\ describe $', fontdict={'size': 16, 'color': 'r'})
	
	n = 1024
	xpot = np.random.normal(0, 1, n)
	ypot = np.random.normal(0, 1, n)
	T = np.arctan2(xpot, ypot)
	
	plt.scatter(xpot, ypot, s=3, c=T, alpha=0.5)
	
	plt.show()

if __name__ == '__main__':
	print(__doc__ % __author__)
	
#	print(df1)
#	print(df2)
#	axis()
#	ignore()
#	join()
#	join_axes()
#	append()
	
#	merge1()	
#	merge2()
	
	plot()
