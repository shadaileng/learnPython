#!/usr/bin/python3
#-*- coding: utf-8 -*-
'''
	****************
	* Web App     *
	****************
	powered by %s
'''

__author__ = 'Shadaileng'
import logging; logging.basicConfig(level=logging.INFO)

import asyncio, inspect, os, json, time
from aiohttp import web
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

def index(request):
	return web.Response(body=b'<h1>Index</h1>', content_type='text/html')


def add_route(app, fn):
	method = getattr(fn, '__method__', None)
	path = getattr(fn, '__route__', None)
	if method is None or path is None:
		raise ValueError('@get or @post is not define at %s' % str(fn))
	print('func: %s, method: %s, path: %s' % (fn.__name__, method, path))
	if not asyncio.iscoroutinefunction(fn) and not inspect.isgeneratorfunction(fn):
		fn = asyncio.coroutine(fn)
	app.router.add_route(method, path, fn)

def add_routes(app, module_name):
	n = module_name.rfind('.')
	if n == -1:
		mod = __import__(module_name, globals(), locals())
	else:
		name = module_name[n + 1:]
		mod = getattr(__import__(module_name[:n], globals, locals(), [name]), name)
	for attr in dir(mod):
		if attr.startswith('_'):
			continue
		fn = getattr(mod, attr)
		if callable(fn):
			method = getattr(fn, '__method__', None)
			path = getattr(fn, '__route__', None)
			if method and path:
				add_route(app, fn)
@asyncio.coroutine
def logger_factory(app, handler):
	def logger(request):
		logging.info('Request: %s %s' % (request.method, request.path))
		return (yield from handler(request))
	return logger

def init_jinja2(app, **kw):
	logging.info('init jinja2 ...')
	options = dict(
		autoescape = kw.get('autoescape', True),
		block_start_string = kw.get('block_start_string', '{%'),
		block_end_string = kw.get('block_end_string', '%}'),
		variable_start_string = kw.get('variable_start_string', '{{'),
		variable_end_string = kw.get('variable_end_string', '}}'),
		auto_reload = kw.get('auto_reload', True)
	)
	path = kw.get('path', None)
	if path is None:
		path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
	logging.info('set jinja2 template path: %s' % path)
	env =Environment(loader=FileSystemLoader(path), **options)
	filters = kw.get('filters', None)
	if filters is not None:
		for name, filter_ in filters.items():
			env.filters[name] = filter_
	app['__templating__'] = env
	
def datetime_filter(t):
	delta = int(time.time() - t)
	if delta < 60:
		return '1分钟前'
	if delta < 3600:
		return '%s分钟前' % (delta // 60)
	if delta < 86400:
		return '%s小时前' % (delta // 3600)
	if delta < 604800:
		return '%s天前' % (delta // 86400)
	dt = datetime.fromtimestamp(t)
	return '%s年%s月%s日' % (dt.year, dt.month, dt.day)

@asyncio.coroutine
def response_factory(app, handler):
	@asyncio.coroutine
	def response(request):
		logging.info('Response handler ...')
		rep = yield from handler(request)
		if isinstance(rep, web.StreamResponse):
			return rep
		if isinstance(rep, bytes):
			rep = web.Response(body=rep)
			rep.content_type = 'application/octet-stream'
			return rep
		if isinstance(rep, str):
			if rep.startswith('redirect:'):
				rep = web.HTTPFound(rep[9:])
			else:
				rep = web.Response(body=rep.encode('utf-8'))
				rep.content_type = 'text/html;charset=utf-8'
			return rep
		if isinstance(rep, dict):
			template = rep.get('__template__')
			if template is None:
				rep = web.Response(body=json.dump(rep, ensure_ascii=False, default = lambda o: o.__dict__).encode('utf-8'))
				rep.content_type = 'application/json;charset=utf-8'
				return rep
			else:
				rep = web.Response(body=app['__templating__'].get_template(template).render(**rep).encode('utf-8'))
				rep.content_type = 'text/html;charset=utf-8'
				return rep
		if isinstance(rep, int) and rep >= 100 and rep < 600:
			return web.Response(rep)
		if isinstance(rep, tuple) and len(r) == 2:
			t, m = rep
			if isinstance(t, int) and t >= 100 and t < 600:
				rep = web.Response(t, str(m))
				return rep
		else:
			rep = web.Response(body=str(r).encode('utf-8'))
			rep.content_type = 'text/plain;charset=utf-8'
			return rep
	return response
		
def add_static(app):
	path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
	app.router.add_static('/static/', path)
	logging.info('add static %s => %s' % ('/static/', path))


@asyncio.coroutine
def init(loop):
	app = web.Application(loop=loop, middlewares = [logger_factory, response_factory])
	init_jinja2(app, filters=dict(datetime=datetime_filter))
	app.router.add_route('GET', '/', index)
	add_routes(app, 'web_handlers')
	add_static(app)
	srv = yield from loop.create_server(app.make_handler(), '127.0.0.1', 8080)
	logging.info('server started at 127.0.0.1:8080')
	
	return srv

def startServer():
	loop = asyncio.get_event_loop()
	loop.run_until_complete(init(loop))
	loop.run_forever()

if __name__ == '__main__':
	print(__doc__ % __author__)
	
	startServer()
