#!usr/bin/python3
#-*- coding: utf-8 -*-

"""
	******************
	*   Webcrawler   *
	******************
	     Powered By %s
"""

__author__ = 'Shadaileng'

from urllib import request, parse
from bs4 import BeautifulSoup
import re, requests, os, sqlite3, sys
sys.setrecursionlimit(1000000)

def catch_urllib(url):
	req = request.Request(url)
	with request.urlopen(req) as f:
		data = f.read()
		print('============Status============')
		print('status: %s - %s' % (f.status, f.reason))
		print('============Header============')
		for k, v in f.getheaders():
			print('%s: %s' % (k, v))
		print('============ Data=============')
		soup = BeautifulSoup(data.decode('utf-8'), features='lxml')
		sub_url = soup.find_all('a',{'target': '_blank', 'href': re.compile('^/item/*')})
		if len(sub_url) > 0:
			for item in sub_url:
				print(item['href'])
		
def weibo(url):
	email = 'qpf0510@sina.com'
	password = '3868865439199248'
	login_data = parse.urlencode([('username', email), ('password', password), ('entry', 'mweibo'), ('cliend_id', ''), ('savestate', '1'), ('ec', ''), ('pagerefer', 'https://passport.weibo.cn/signin/welcome?entry=mweibo&r=http%3A%2F%2Fm.weibo.cn%2F')])
	req = request.Request(url)
	req.add_header('Origin', 'https://passport.weibo.cn')
	req.add_header('User-Agent', 'Mozilia/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
	req.add_header('Referer', 'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F')
	with request.urlopen(req, data=login_data.encode('utf-8')) as f:
		data = f.read()
		print('============Status============')
		print('status: %s - %s' % (f.status, f.reason))
		print('============Header============')
		for k, v in f.getheaders():
			print('%s: %s' % (k, v))
		print('============Data============\n%s' % data.decode('utf-8'))


def catch_requests(url, node, node_condition, dir_ = './res/img/'):
	os.makedirs(dir_, exist_ok = True)
	rep = requests.get(url, allow_redirects=True)
	print('status: %s, reason: %s' % (rep.status_code, rep.reason))
	if rep.status_code == 200:
		data = rep.content.decode('utf-8')
		soup = BeautifulSoup(data, features='lxml')
		items = soup.find_all(node, node_condition)
		for item in items:
			for img in item.find_all('img'):
				url = img['src']
				print('get img: %s' % url)
				res = requests.get(url, stream = True)
				print('status: %s, reason: %s' % (res.status_code, res.reason))
				if res != None:
					name = url.split('/')[-1] 
					same = saveData(name=name, url=url, path=dir_+name)
					if not same:
						with open(dir_ + name, 'wb') as f:
							for chunk in res.iter_content(chunk_size=128):
								f.write(chunk)
							print('Save %s as %s' % (url, name))
					else:
						print('exist img: %s' % url)

def saveData(name = None, url = None, path = None, db = './res/img_data.db'):
	conn = None
	same = True
	try:
		conn = sqlite3.connect(db)
	except Exception as e:
		print(e)
		conn = None
	if not conn:
		print('Failed to connect db: %s success' % db)
		return conn
	try:
		with conn as conn_:
			cursor = conn_.cursor()
			cursor.execute('select * from imgs where name = "%s" and url = "%s" ' % (name, url))
			res = list(row for row in cursor.fetchall())
			if len(res) <= 0:
				same = False
				conn_.execute('insert into imgs(name, url, path) values("%s", "%s", "%s")' % (name, url, path))
				change = conn_.total_changes
				print('change %s' % change)
#			cursor.execute('select * from imgs')
#			res = cursor.fetchall()
#			print(res)
	except (sqlite3.OperationalError, sqlite3.IntegrityError) as e:
		print(e)
	if conn is not None:
		cursor.close()
		conn.close()
		cursor = None
		conn = None
		print('close %s, %s' % (cursor, conn))
	return same
	


def redict_requests(url, node, node_condition, page = -1):
	print('redict to %s' % url)
	catch_requests(url, 'div', {'id': 'main-2'})
	rep = requests.get(url, allow_redirects=True)
	print('status: %s, reason: %s' % (rep.status_code, rep.reason))
	if rep.status_code == 200:
		data = rep.content.decode('utf-8')
		soup = BeautifulSoup(data, features='lxml')
		items = soup.find_all(node, node_condition)
		for item in items:
			for a in item.find_all('a'):
				href = a['href']
				if page > 0:
					if(int(href.split('/')[-1]) < page):
						redict_requests(href, node, node_condition)
				else:
					redict_requests(href, node, node_condition)

def executeSql(sql, db = './res/img_data.db'):
	conn = None
	try:
		conn = sqlite3.connect(db)
	except Exception as e:
		print(e)
		conn = None
	if not conn:
		print('Failed to connect db: %s success' % db)
		return conn
	try:
		with conn as conn_:
			cursor = conn_.cursor()
			cursor.execute(sql)
			res = cursor.fetchall()
			for row in res:
				print(row)
	except (sqlite3.OperationalError, sqlite3.IntegrityError) as e:
		print(e)
	if conn is not None:
		cursor.close()
		conn.close()
		cursor = None
		conn = None
		print('close %s, %s' % (cursor, conn))
	

if __name__ == '__main__':
#	catch_urllib('https://baike.baidu.com')
#	weibo('https://passport.weibo.cn/sso/login')
#	catch_requests('http://www.nationalgeographic.com.cn/animals/', 'ul', {'class': 'img_list'})

#	catch_requests('http://moeimg.net/', 'div', {'id': 'main-2'})
#	saveData(name='a', url='b', './res/img/a')

	redict_requests('http://moeimg.net/', 'li', {'class': 'next'})

#	executeSql('create table imgs(name varchar(256), url varchar(256), path varchar(256))')
#	executeSql('select * from imgs')
#	executeSql('delete from imgs')
