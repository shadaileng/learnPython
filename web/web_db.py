#!/usr/bin/python3
#-*- coding: utf-8 -*-
'''
	****************
	* Web DB     *
	****************
	powered by %s
'''

__author__ = 'Shadaileng'
import logging; logging.basicConfig(level=logging.INFO)
import sqlite3, asyncio

__count = 0

#@asyncio.coroutine
def create_sqlite_connect(db = 'test.db', max = 10):
	global __count
	__count = __count + 1
	try:
		print('Current Connect: %s' % __count)
		if __count <= max:
			conn = sqlite3.connect(db)
			return conn
		else:
			raise ConnExcept('full connection')
	except BaseException as e:
		print(e)
		return None

def select(sql, args, size = None):
	print(sql, args)
	conn = create_sqlite_connect()
	try:
		with conn:
			cur = conn.cursor()
			cur.execute(sql.replace('?', '%s'), args or ())
			if size:
				return cur.fetchmany(size)
			else:
				return cur.fetchall()
	except (sqlite3.OperationalError, sqlite3.IntegrityError) as e:
		print('Could not complete operation : %s' % e)

def execute(sql, args):
	conn = create_sqlite_connect()
	try:
		with conn:
			conn.execute(sql, args)
			return conn.total_changes
	except (sqlite3.OperationalError, sqlite3.IntegrityError) as e:
		print('Could not complete operation : %s' % e)
	
if __name__ == '__main__':
	print(__doc__ % __author__)
	
	create = 'CREATE TABLE USER(id varchar(10) primary key, name varchar(30), password varchar(16))'
	
	insert = 'INSERT INTO USER(id, name, password) values("3", "Shadaileng", "123123")'
	
#	select = 'select * from USER'
	
#	execute(create)
#	execute(insert)
	execute('update user set name = "qpf" where id = ?', (2,))

	rs = select('select * from USER', (), 4)
	for row in rs:
		print(row)

