#!/usr/bin/python3
#-*- coding: utf-8 -*-
'''
	***********
	* master *
	***********
	powered by %s
'''

__author__ = 'Shadaileng'

import queue
from multiprocessing.managers import BaseManager

send_task = queue.Queue()
recv_task = queue.Queue()

class QueueManager(BaseManager):
	pass

QueueManager.register('get_send_task', callable = lambda: send_task)
QueueManager.register('get_recv_task', callable = lambda: recv_task)

manager = QueueManager(address=('', 5000), authkey=b'abc')


if __name__ == '__main__':
	
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
