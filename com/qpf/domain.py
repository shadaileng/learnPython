#!/usr/bin/python3
#-*- coding: utf-8 -*-
'''
	***************************
	* domain define the class *
	***************************
	powered by %s
'''
__author__ = 'Shadaileng'

class Person(object):
	def __init__(self, name, age):
		self.__name = name
		self.__age = age
	@property
	def name(self):
		return self.__name
	@name.setter
	def name(self, name):
		self.__name = name
	@property
	def age(self):
		return self.__age
	@age.setter
	def age(self, age):
		self.__age = age
	def __str__(self):
		return '<Person object %s>' % self.__dict__
	__repr__ = __str__

if __name__ == '__main__':
	print(__doc__ % __author__)
	shadaileng = Person('Shadaileng', 25)
	print(shadaileng.name)
