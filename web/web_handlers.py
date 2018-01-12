#!/usr/bin/python3
#-*- coding: utf-8 -*-
'''
	****************
	* handlers    *
	****************
	powered by %s
'''

__author__ = 'Shadaileng'

import logging; logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(filename)s line:%(lineno)d %(message)s')
import functools, time, re, json, hashlib, base64
from aiohttp import web
from web_domain import User, Blog, next_id
from web_handlers_base import get, post, user2cookie

COOKIE_NAME = 'shadaileng'

_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'[0-9a-f]{40}$')


@get('/')
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

@get('/register')
def redirect_register(request):
	return {
		'__template__': 'register.html'
	}

@post('/api/users')
def api_register_user(*, name, email, password):

	logging.info('args:', name, email, password)
	
	if not name or not name.strip():
		raise Exception('name is null')
	if not email or not _RE_EMAIL.match(email):
		raise Exception('email is not format')
	if not password:
		raise Exception('password is null')
	users = yield from User(email=email).find()
	logging.info('users: %s' % users)
	if users is not None:
		raise Exception('email: %s is in use' % email)
	uid = next_id()
	sha1_passwd = '%s-%s' % (uid, password)
	
	user = User(id=uid, name=name, password=hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest(), email=email, admin='0', image='../res/tumblr.png', )
	res = yield from user.save()
	if res == 1:
		logging.info('register successed')
	else:
		logging.info('register failed')
	rep = web.Response()
	rep.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
	user.password = '******'
	rep.content_type = 'application/json'
	rep.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
	
	return rep


@get('/signin')
def redirect_login(request):
	return {
		'__template__': 'login.html'
	}

@post('/api/authenticate')
def authenticate(*, email, password):
	if not email:
		raise Exception('email is null')
	if not password:
		raise Exception('password is null')
	users = yield from User(email=email).find()
	if len(users) == 0:
		raise Exception('user is not exist')
	user = users[0]
	
	sha1_passwd = '%s-%s' % (user.id, password)
	sha1 = hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest()
	
	if user.password != sha1:
		logging.info('==password: %s===' % user.password)
		logging.info('==sha1: %s===' % sha1)
		raise Exception('password is wrong')
	user.password = '******'
	rep = web.Response()
	rep.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
	rep.content_type = 'application/json'
	rep.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
	
	return rep
	
@get('/signout')
def signout(request):
	referer = request.headers.get('Referer')
	rep = web.Response(referer or '/')
	rep.set_cookie(COOKIE_NAME, '-delete-', max_age=0, httponly=True)
	logging.info('user signout')
	
	return rep

@get('/create_blogs')
def redirect_create_blogs(request):
	return {
		'__template__': 'create_blog.html'
	}
@post('/api/blogs')
def api_create_blog(*, name, summary, content):
	if not name or not name.strip():
		raise Exception('name is null')
	if not summary or not summary.strip():
		raise Exception('summary is null')
	if not content or not content.strip():
		raise Exception('content is null')
	
	blog = Blog(user_id = request.__user__.id, name = name.strip(), summary = summary.strip(), content = content.strip())
	res = yield from Blog.save()
	if res == 1:
		logging.info('create_blog successed')
	else:
		logging.info('create_blog failed')
	
	rep = web.Response()
	rep.content_type = 'application/json'
	rep.body = json.dumps(blog, ensure_ascii=False).encode('utf-8')
	
	return rep

if __name__ == '__main__':
	pass
