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
	
	
