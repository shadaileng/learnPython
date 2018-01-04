#!/usr/bin/python3
#-*- coding: utf-8 -*-
'''
	****************
	* Test       *
	****************
	powered by %s
'''

__author__ = 'Shadaileng'

import os




if __name__ == '__main__':
	print(__doc__ % __author__)
	
	print(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template'))
