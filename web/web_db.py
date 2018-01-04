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
		logging.info('Current Connect: %s' % __count)
		if __count <= max:
			conn = sqlite3.connect(db)
		else:
			raise ConnExcept('full connection')
	except BaseException as e:
		logging.info(e)
		conn = None
	if conn:
		logging.info('Connect success')
	return conn

def select(sql, args, size = None):
	logging.info('%s %s' % (sql, args))
	conn = create_sqlite_connect()
	try:
		with conn:
			cur = conn.cursor()
			cur.execute(sql, args or ())
			if size:
				rs = cur.fetchmany(size)
			else:
				rs = cur.fetchall()
	except (sqlite3.OperationalError, sqlite3.IntegrityError) as e:
		logging.error('Could not complete operation : %s' % e)
	cur.close()
	logging.warn('return result: %s' % len(rs))
	return rs
	
def execute(sql, args):
	logging.info('%s %s' % (sql, args))
	conn = create_sqlite_connect()
	try:
		with conn:
			conn.execute(sql, args)
	except (sqlite3.OperationalError, sqlite3.IntegrityError) as e:
		print('Could not complete operation : %s' % e)
	return conn.total_changes
	
if __name__ == '__main__':
	print(__doc__ % __author__)
	
	create = 'CREATE TABLE USER(id varchar(10) primary key, name varchar(30), password varchar(16))'
	
	insert = 'INSERT INTO USER(id, name, password) values("3", "Shadaileng", "123123")'
	
#	select = 'select * from USER'
	
#	execute(create)
#	execute(insert)
#	execute('drop table user', [])
#	execute('create table user(id varchar(50) primary key, name varchar(50), password varchar(50), email varchar(50), admin varchar(1), image varchar(500), create_time varchar(50))', [])
#	execute('create table blog(id varchar(50) primary key, name varchar(50), user_id varchar(50), summary varchar(50), content varchar(1500), create_time varchar(50))', [])
#	execute('create table comment(id varchar(50) primary key, blog_id varchar(50), user_id varchar(50), content varchar(500), create_time varchar(50))', [])
#	execute('delete from user', [])
	
	rs = select('select * from USER', [])
	
	for row in rs:
		print(row)	
'''
	rs = select('select name from sqlite_master where type = "table"', (), 4)
	for row in rs:
		print(row)
	
	execute('update user set name = "qpf" where id = ?', (2,))
	rs = select('select * from USER', (), 4)
	for row in rs:
		print(row)
'''
