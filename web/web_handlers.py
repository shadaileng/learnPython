#!/usr/bin/python3
#-*- coding: utf-8 -*-
'''
	****************
	* handlers    *
	****************
	powered by %s
'''

__author__ = 'Shadaileng'

import functools
from aiohttp import web
from web_domain import User

def get(path):
	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args, **kw):
			return func(*args, **kw)
		wrapper.__method__ = 'GET'
		wrapper.__route__ = path
		return wrapper
	return decorator

def post(path):
	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args, **kw):
			return func(*args, **kw)
		wrapper.__method__ = 'POST'
		wrapper.__route__ = path
		return wrapper
	return decorator


@get('/blog')
def hello(request):
	print('hello')
	return web.Response(body=b'<h1>hello</h1>', content_type='text/html')
	
@get('/user')
def bye(request):
	print('bye ')
	return web.Response(body=b'<h1>bye</h1>', content_type='text/html')
	
@get('/test')
def bye(request):
	users = User().find()
	print('get users: ' )
	for user in users:
		print('name: %s, email: %s' % (user.name, user.email))
	return {
		'users': users,
		'__template__': 'test.html'
	}

if __name__ == '__main__':
	add_routes(None, 'web_handlers')
