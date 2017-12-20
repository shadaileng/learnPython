#!/usr/bin/python3
#-*- coding: utf-8 -*-

import os
from multiprocessing import Process,Pool,Queue
import time, random, subprocess, threading
'''
	Unix OS multiProcess
'''
def ufork():
	print('process start at %s' % os.getpid())
	pid = os.fork()
	if pid == 0:
		print('current process %s, create by process %s' % (os.getpid(), os.getppid()))
	else:
		print('current process %s, creat a process %s' % (os.getpid(), pid))
'''
	crass os multiProcess
'''
def child_run(name):
	print('%s process %s, create by process %s' % (name, os.getpid(), os.getppid()))

def multiProcess():
	print('process start at %s' % os.getpid())
	p = Process(target=child_run, args=('child', ))
	print('start the child process')
	p.start()
	p.join()
	print('parent process end')
	
'''
	processPool
'''
def longtimetask(name):
	s = time.time()
	time.sleep(3)
	e = time.time()
	print('Task %s sleep %0.3f second.' % (name, e -s))
	
def processPool():
	print('process start in %s' % os.getpid())
	p = Pool(4)
	for i in range(5):
		p.apply_async(longtimetask, (i,))
	p.close()
	p.join()
	print('process end')
	
'''
	subProcess
'''
	
def subProcess():
	'''
	print('process start in %s, subProcess: ping -c 3 www.baidu.com' % os.getpid())
	r = subprocess.call(['ping', '-c', '3', 'www.baidu.com'])
	print('repo: %s' % r)
	'''
	print('process start in %s, subProcess: python' % os.getpid())
	p = subprocess.Popen(['python'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, err = p.communicate(b'1+1\nexit()')
	print(output.decode('utf-8'))
	print('repoCode:', p.returncode)
	
'''
	Queue
'''
def writep(q):
	print('write:')
	for i in range(5):
		print('write:', i)
		q.put(i)
		time.sleep(1)
	
	print('write quit')
	
def readp(q):
	while True:
		r = q.get()
		print('read:', r)
def queuerw():
	q = Queue()
	wp = Process(target=writep, args=(q,))
	rp = Process(target=readp, args=(q,))
	wp.start()
	rp.start()
	wp.join()
	rp.terminate()
	
def looping():
	print('Thread %s is running' % threading.current_thread().name)
	for i in range(10):
		print('Thread %s: %s'  % (threading.current_thread().name, i))
		time.sleep(random.random() * 3)
	print('Thread %s end' % threading.current_thread().name)
	
def thread():
	print('Thread %s is running' % threading.current_thread().name)
	t = threading.Thread(target=looping, name='subthread')
	t.start()
	t.join()
	print('Thread %s end' % threading.current_thread())
	
