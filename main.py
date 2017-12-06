#!/usr/bin/python3
#-*- coding: utf-8 -*-
'''
	***************
	* Main module *
	***************
	powered by %s
'''

__author__ = 'Shadaileng'


from process_test import ufork, multiProcess, processPool,subProcess,queuerw, thread

from datetime import datetime

if __name__ == '__main__':
	print(__doc__  % __author__)
	print('********IO************')
	#io - picking
	from io_test import picking
	picking()	
	print('********Process************')
	#ufork()
	
	#multiProcess()
	
	#processPool()
	
	#subProcess()
	
	#queuerw()
	
	#thread()
	
	now = datetime.now()
	print('now:', now, now.timestamp())
	
	custom = datetime(2020, 12, 25, 5, 5)
	custom_t = custom.timestamp()
	
	print('origin:', custom, '\ntimestamp:', custom_t, '\nfromtimestamp:', datetime.fromtimestamp(custom_t), '\nutcfromtimestamp', datetime.utcfromtimestamp(custom_t))
	
	strtime = datetime.strptime('2017-12-25 05:05:00', '%Y-%m-%d %H:%M:%S')
	
	print('str2time:', strtime)
	print('time2str:', strtime.strftime('%Y-%m-%d %H:%M:%S'))
