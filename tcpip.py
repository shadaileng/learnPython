#!/usr/bin/python3
#-*- coding: utf-8 -*-
'''
	*************************
	* TCP/IP module *
	*************************
	powered by %s
'''

__author__ = 'Shadaileng'

import socket, threading, sys, time

def connectBaidu():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('www.baidu.com', 80))
	s.send(b'GET / HTTP/1.1\r\nHost:www.baidu.com\r\nConnection: close\r\n\r\n')

	buf = []
	while True:
		d = s.recv(1024)
		if d:
			buf.append(d)
		else:
			break
	data = b''.join(buf)
	s.close()

	header, html = data.split(b'\r\n\r\n')
	print(header.decode('utf-8'))

	with open('./res/baidu.html', 'wb') as f:
		f.write(html)
		
def tcp_server():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('127.0.0.1', 9999))
	s.listen(5)
	print('server is listening port 9999...')
	while True:
		sock, addr = s.accept()
		t = threading.Thread(target=server_connection, args=(sock, addr))
		t.start()
def server_connection(sock, addr):
	print('connecting the client: %s:%s...' % addr)
	sock.send(b'connect success.')
	while True:
		data = sock.recv(1024)
		time.sleep(1)
		if not data or data.decode('utf-8') == 'exit':
			break
		print('%s: %s' % (addr, data.decode('utf-8')))
		sock.send(b'Hello')
	sock.close()
	print('connection %s:%s is closed.' % addr)
	
def tcp_client():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('127.0.0.1', 9999))
	for data in ['Shadaileng', 'qpf', 'Chik']:
		s.send(data.encode('utf-8'))
		print('server: %s' % s.recv(1024).decode('utf-8'))
	s.send(b'exit')
	s.close()
	
if __name__ == '__main__':
	if	sys.argv[1] == '0':
		tcp_server()
	elif sys.argv[1] == '1':
		tcp_client()
