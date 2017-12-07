#!/usr/bin/python3
#-*- coding: utf-8 -*-
'''
	***************
	* inbuild module *
	***************
	powered by %s
'''

if __name__ == '__main__':
	print('*********datetime*****************')
	from datetime import datetime, timedelta, timezone

	now = datetime.now()
	print('now:', now, now.timestamp())
	
	custom = datetime(2020, 12, 25, 5, 5)
	custom_t = custom.timestamp()
	
	print('origin:', custom, '\ntimestamp:', custom_t, '\nfromtimestamp:', datetime.fromtimestamp(custom_t), '\nutcfromtimestamp', datetime.utcfromtimestamp(custom_t))
	
	strtime = datetime.strptime('2017-12-25 05:05:00', '%Y-%m-%d %H:%M:%S')
	
	print('str2time:', strtime)
	print('time2str:', strtime.strftime('%Y-%m-%d %H:%M:%S'))
	
	print('yesterday:', now - timedelta(days=1))
	
	tz_utc8 = timezone(timedelta(hours=8))
	now.replace(tzinfo=tz_utc8)
	print('now_utc8:', now)
	
	print('*********base64*******************')
	import base64
	
	str64 = base64.b64encode(b'base64\x00str')
	strn = base64.b64decode(str64)
	print('str64: %s\nstr: %s' % (str64, strn))
	
	print('*********hashlib*****************')
	import hashlib
	
	def str2md5(s):
		md5 = hashlib.md5()
		md5.update(s.encode('utf-8'))
		return md5.hexdigest()
	
	print('Hello: %s' % str2md5('Hello'))
	print('hello: %s' % str2md5('hello'))
	
	def str2sha1(s):
		sha1 = hashlib.sha1()
		sha1.update(s.encode('utf-8'))
		return sha1.hexdigest()
		
	print('Hello: %s' % str2sha1('Hello'))
	print('hello: %s' % str2sha1('hello'))
	
	db = {}
	
	def register(name, passwd):
		db[name] = str2md5(name + passwd)
	def login(name, passwd):
		if db[name] == str2md5(name + passwd):
			print('登陆成功')
		else:
			print('密码错误')
	register('shadaileng', '3868865439')
	login('shadaileng', '3868865439')
	login('shadaileng', '38688654391')
	
	print('*********urllib*****************')
	from urllib import request
	with request.urlopen('http://www.baidu.com') as f:
		data = f.read()
		print('Status:', f.status, f.reason)
		for k, v in f.getheaders():
			print('%s: %s' % (k, v))
		print('Data: ', data.decode('utf-8'))
	
	print('*********HTMLParser*****************')
	from html.parser import HTMLParser
	from html.entities import name2codepoint
	
	class MyHTMLParser(HTMLParser):
		def handle_starttag(self, tag, attrs):
			print('<%s>' % tag)
		def handle_endtag(self, tag):
			print('</%s>' % tag)
		def handle_startendtag(self, tag, attrs):
			print('<%s>' % tag)
		def handle_data(self, data):
			print(data)
		def handle_comment(self, data):
			print('<!-- %s -->' % data)
		def handle_entityref(self, name):
			print('&%s;' % name)
		def handle_charref(self, name):
			print('&#%s;' % name)
	parser = MyHTMLParser()
	data = r'''
	<html>
		<head>
			<title>Hello</title>
		<head>
		<body>
			<a href='#'>page</a>
			<h1>Hello
		<body>
	</html>
	'''
	parser.feed(data)
	
			
			
	
