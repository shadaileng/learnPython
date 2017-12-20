#!/usr/bin/python3
#-*- coding: utf-8 -*-
'''
	***********
	* master *
	***********
	powered by %s
'''

__author__ = 'Shadaileng'

import queue, time, sys
from multiprocessing.managers import BaseManager

class QueueManager(BaseManager):
	pass

def server():
	
	send_task = queue.Queue()
	recv_task = queue.Queue()

	QueueManager.register('get_send_task', callable = lambda: send_task)
	QueueManager.register('get_recv_task', callable = lambda: recv_task)

	manager = QueueManager(address=('', 5000), authkey=b'abc')
	
	manager.start()
	send = manager.get_send_task()
	recv = manager.get_recv_task()

	for i in range(10):
		print('put %d to send' % i)
		send.put(i)
	print('master wait recv ...')

	for i in range(10):
		result = recv.get(timeout=10)
		print('master recv: %s' % result)
	
	manager.shutdown()
	print('master exit.')

def client():
	QueueManager.register('get_send_task')
	QueueManager.register('get_recv_task')

	server_addr = '127.0.0.1'
	print('connect to %s' % server_addr)

	m = QueueManager(address=(server_addr, 5000), authkey=b'abc')
	
	m.connect()

	send = m.get_send_task()
	recv = m.get_recv_task()

	for i in range(10):
		try:
			n = send.get(timeout=1)
			print('worker recv: %s' % n)
			r = '%d * %d = %d' % (n, n, n * n)
			time.sleep(1)
			print('worker send:%s' % r)
			recv.put(r)
		except Exception as e:
			print('Error: %s' % e)
	print('worker exit.')

if __name__ == '__main__':
	if sys.argv[1] == '1':
		client()
	elif sys.argv[1] == '0':
		server()
