#!/usr/bin/python3
#-*- coding: utf-8 -*-
'''
	**********************
	* handlers base    *
	**********************
	powered by %s
'''

__author__ = 'Shadaileng'

import logging; logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(filename)s line:%(lineno)d %(message)s')
import inspect, functools, asyncio, time, hashlib
from urllib import parse
from web_config_default import configs
from web_domain import User

from aiohttp import web


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

_COOKIE_KEY = configs.session.flag

COOKIE_NAME = 'shadaileng'

def user2cookie(user, max_age):
	duration = str(int(time.time() + max_age))
	cookies = '%s-%s-%s-%s' % (user.id, user.password, duration, _COOKIE_KEY)
	
	return '-'.join([user.id, duration, hashlib.sha1(cookies.encode('utf-8')).hexdigest()])

@asyncio.coroutine
def cookie2user(cookies):
	if not cookies:
		return None
	
	try:
		L = cookies.split('-')
		if len(L) != 3:
			return None
		uid, duration, sha1 = L
		if int(duration) < time.time():
			return None
		user = yield from User(id=uid).find()
		if user is None:
			return None
		user = user[0]
		s = '%s-%s-%s-%s' % (user.id, user.password, duration, _COOKIE_KEY)
		if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
			logging.info('sha1 error')
			return None
		user.password = '******'
		return user
	except Exception as e:
		logging.exception(e)
		return None

@asyncio.coroutine
def auth_factory(app, handler):
	@asyncio.coroutine
	def auth(request):
		logging.info('check user: %s %s' % (request.method, request.path))
		request.__user__ = None
		cookies = request.cookies.get(COOKIE_NAME)
		if cookies:
			user = yield from cookie2user(cookies)
			if user:
				logging.info('set current user: %s' % user.email)
				request.__user__ = user
				logging.info('%s.request: %s' % (handler.__name__, request))
		return (yield from handler(request))
	return auth

def get_required_kw_args(fn):
	args = []
	params = inspect.signature(fn).parameters
	for name, param in params.items():
		if param.kind == inspect.Parameter.KEYWORD_ONLY and param.default == inspect.Parameter.empty:
			args.append(name)
	return tuple(args)

def get_named_kw_args(fn):
	args = []
	params = inspect.signature(fn).parameters
	for name, param in params.items():
		if param.kind == inspect.Parameter.KEYWORD_ONLY:
			args.append(name)
	return tuple(args)


def has_named_kw_args(fn):
	params = inspect.signature(fn).parameters
	for name, param in params.items():
		if param.kind == inspect.Parameter.KEYWORD_ONLY:
			return True

def has_var_kw_arg(fn):
	params = inspect.signature(fn).parameters
	for name, param in params.items():
		if param.kind == inspect.Parameter.VAR_KEYWORD:
			return True

def has_request_arg(fn):
	sig = inspect.signature(fn)
	params = sig.parameters
	found = False
	for name, param in params.items():
		if name == 'request':
			found = True
			continue
		if found and (param.kind != inspect.Parameter.VAR_POSITIONAL and param.kind != inspect.Parameter.KEYWORD_ONLY and param.kind != inspect.Parameter.VAR_KEYWORD):
			raise ValueError('request parameter must be the last named parameter in function : %s%s' % (fn.__name__, str(sig)))
	return found

class RequestHandler(object):
	def __init__(self, app, fn):
		self._app = app
		self._func = fn
		self._has_request_arg = has_request_arg(fn)
		self._has_var_kw_arg = has_var_kw_arg(fn)
		self._has_named_kw_args = has_named_kw_args(fn)
		self._named_kw_args = get_named_kw_args(fn)
		self._required_kw_args = get_required_kw_args(fn)
	
	@asyncio.coroutine
	def __call__(self, request):
		kw = None
		if self._has_var_kw_arg or self._has_named_kw_args or self._has_request_arg:
			if request.method == 'POST':
				if not request.content_type:
					return web.HTTPBadRequest('Missing Content-Type.')
				ct = request.content_type.lower()
				if ct.startswith('application/json'):
					params = yield from request.json()
					if not isinstance(params, dict):
						return web.HTTPBadRequest('JSON budy must be object')
					kw = params
				elif ct.startswith('application/x-www-form-urlencoded') or ct.startswith('multipart/form-data'):
					params = yield from request.post()
					kw = dict(**params)
				else:
					return web.HTTPBadRequest('Unsupported Content-Type: %s' % request.content_type)
			if request.method == 'GET':
				qs = request.query_string
				if qs:
					kw = dict()
					for k, v in parse.parse_qs(qs, True).items():
						kw[k] = v[0]
		if kw is None:
			kw = dict(**request.match_info)
		else:
			if not self._has_var_kw_arg and self._has_named_kw_args:
				copy = dict()
				for name in self._named_kw_args:
					if name in kw:
						copy[name] = kw[name]
				kw = copy
			for k, v in request.match_info.items():
				if k in kw:
					logging.warning('arg both in named parameter and kw')
				kw[k] = v
		if self._has_request_arg:
			kw['request'] = request
		if self._required_kw_args:
			for name in self._required_kw_args:
				if not name in kw:
					return web.HTTPBadRequest('Missing argument: %s' % name)
		logging.info('%s call with args: %s' % (self._func.__name__, str(kw)))
		try:
			rep = yield from self._func(**kw)
			return rep
		except Exception as e:
			logging.exception('====================')
			return dict(error = e)

