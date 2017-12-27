#!/usr/bin/python3
#-*- coding: utf-8 -*-
'''
	***************
	* Async     *
	***************
	powered by %s
'''

__author__ = 'Shadaileng'

from com.qpf.qpf_log import log_time_data

import asyncio

from aiohttp import web

def handle():
	r = ''
	while True:
		n = yield r
		if not n:
			return
		log_time_data('recv: %s' % n)
		r = '200 ok'
		
def sender(handle):
	handle.send(None)
	n = 0
	while n < 5:
		n+=1
		log_time_data('send: %s' % n)
		r = handle.send(n)
		log_time_data('return: %s' % r)
	handle.close()
#使用注解将generate标记为coroutine
@asyncio.coroutine
def hello(last):
	log_time_data('Hello 1 last: %s' % last)
	r = yield from asyncio.sleep(last)
	log_time_data('Hello 2 last: %s' % last)

def asyncio_test():
	loop = asyncio.get_event_loop()
	tasks = [hello(1), hello(2)]
	#消息循环中任务之间不会形成阻塞，遇到yield在任务内等待，跳转执行另一任务，直到返回结果才继续执行任务。
	loop.run_until_complete(asyncio.wait(tasks))
	
	loop.close()

@asyncio.coroutine
def wget(host):
	log_time_data('wget: %s' % host)
	connect = asyncio.open_connection(host, 80)
	reader, writer = yield from connect
	
	header = 'GET / HTTP/1.0\r\nHost:%s\r\n\r\n' % host
	writer.write(header.encode('utf-8'))
	yield from writer.drain()
	while True:
		line = yield from reader.readline()
		if line == b'\r\n':
			break
		log_time_data('%s header > %s' % (host, line.decode('utf-8').rstrip()))
	writer.close()

def asyncio_test_wget():
	loop = asyncio.get_event_loop()
	tasks = [wget(host) for host in ['www.baidu.com', 'www.qq.com', 'www.163.com']]
	loop.run_until_complete(asyncio.wait(tasks))
	loop.close()
#async 和 await 只能在pathon3.4之后的版本使用
#使用async代替注解
async def async_await(last):
	log_time_data('Hello 1 last: %s' % last)
	#使用await代替yield
	await asyncio.sleep(1)
	log_time_data('Hello 2 last: %s' % last)
	
def asyncio_test_async_await():
	loop = asyncio.get_event_loop()
	tasks = [async_await(1), async_await(2)]
	loop.run_until_complete(asyncio.wait(tasks))
	loop.close()
#aiohttp
async def index(request):
	await asyncio.sleep(0.5)
	return web.Response(body=b'<h1>Index</h1><a href="/hello/sdl">hello sdl</a>', content_type='text/html')
	
async def hello(request):
	await asyncio.sleep(0.5)
	text = '<h1>Hello %s</h1>' % request.match_info['name']
	return web.Response(body=text.encode('utf-8'), content_type='text/html')	

async def init(loop):
	app = web.Application(loop=loop)
	app.router.add_route('GET', '/', index)
	app.router.add_route('GET', '/hello/{name}', hello)
	srv = await loop.create_server(app.make_handler(), '127.0.0.1', 8080)
	log_time_data('Server started at port 8080 ...')
	return srv
	
def startServer():
	loop = asyncio.get_event_loop()
	loop.run_until_complete(init(loop))
	loop.run_forever()

if __name__ == '__main__':
	print(__doc__  % __author__)
	
#	sender(handle())
	
#	asyncio_test()

#	asyncio_test_wget()

#	asyncio_test_async_await()
	
	startServer()
