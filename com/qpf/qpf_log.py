#!/usr/bin/python3
#-*- coding: utf-8 -*-
'''
	**********
	*  log  *
	**********
	   --powered by %s

'''

__author__ = 'Shadaileng Chik'

from datetime import datetime

def log_time():
	return datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " >>> "

def log_time_data(log):
	print(log_time() + log)

if __name__ == '__main__':
	print(__doc__ % __author__)
	print(log_time())
	log_time_data('Hello World')
