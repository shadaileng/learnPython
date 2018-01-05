#!/usr/bin/python3
#-*- coding: utf-8 -*-
'''
	****************
	* handlers    *
	****************
	powered by %s
'''

__author__ = 'Shadaileng'

import functools, time
from aiohttp import web
from web_domain import User, Blog

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
	summary = "这是一篇博客，我也不知道写的是什么。。。。"
	blogs = [
		Blog(id='1', name='富强 · 民主', summary=summary, create_time=time.time() - 1200),
		Blog(id='2', name='文明 · ,和谐', summary=summary, create_time=time.time() - 3600),
		Blog(id='3', name='自由 · 平等', summary=summary, create_time=time.time() - 4800),
		Blog(id='4', name='公正 · 法制', summary=summary, create_time=time.time() - 84800),
		Blog(id='4', name='爱国 · 敬业', summary=summary, create_time=time.time() - 100000),
		Blog(id='4', name='诚信 · 友善', summary=summary, create_time=time.time() - 653200)
	]
	return {
		'__template__': 'blog.html',
		'blogs': blogs
	}
	
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
