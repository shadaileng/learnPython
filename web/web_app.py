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

import asyncio
from aiohttp import web


def index(request):
	return web.Response(body=b'<h1>Index</h1>', content_type='text/html')

@asyncio.coroutine
def init(loop):
	app = web.Application(loop=loop)
	app.router.add_route('GET', '/', index)
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
