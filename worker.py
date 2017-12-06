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
	client()
