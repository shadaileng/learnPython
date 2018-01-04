#!/usr/bin/python3
#-*- coding: utf-8 -*-
'''
	****************
	* domain     *
	****************
	powered by %s
'''

__author__ = 'Shadaileng'
import logging; logging.basicConfig(level=logging.INFO)
import time
from datetime import datetime
from web_domain_maker import Model, StringField
def next_id():
	return '%015d000' % (time.time() * 1000)
	
class User(Model):
	id = StringField(name = 'id', default = next_id, column_type = 'varchar(50)', primary_key = True)
	name = StringField(name = 'name', column_type = 'varchar(50)')
	password = StringField(name = 'password', column_type = 'varchar(50)')
	email = StringField(name = 'email', column_type = 'varchar(50)')
	admin = StringField(name = 'admin', column_type = 'varchar(1)')
	image = StringField(name = 'image', column_type = 'varchar(500)')
	create_time = StringField(name = 'create_time', column_type = 'varchar(50)', default = datetime.fromtimestamp(time.time()))
	
class Blog(Model):
	id = StringField(name = 'id', default = next_id, column_type = 'varchar(50)', primary_key = True)
	name = StringField(name = 'name', column_type = 'varchar(50)')
	user_id = StringField(name = 'user_id', column_type = 'varchar(50)')
	summary = StringField(name = 'summary', column_type = 'varchar(50)')
	content = StringField(name = 'content', column_type = 'varchar(50)')
	create_time = StringField(name = 'create_time', column_type = 'varchar(50)', default = time.time)

class Comment(Model):
	id = StringField(name = 'id', default = next_id, column_type = 'varchar(50)', primary_key = True)
	blog_id = StringField(name = 'blog_id', column_type = 'varchar(50)')
	user_id = StringField(name = 'user_id', column_type = 'varchar(50)')
	content = StringField(name = 'content', column_type = 'varchar(50)')
	create_time = StringField(name = 'create_time', column_type = 'varchar(50)', default = time.time)

if __name__ == '__main__':
	print(__doc__ % __author__)
#	user = User(name = 'qpf', password = '123456', email = 'qpf0510@qq.com', admin = '0', image = '../res/tumblr.png')
#	print(user.save())
#	User(id = '001514527699550000', name = 'Shdaileng').update()
#	rs = User().find()
#	for row in rs:
#		print(row)	
	user = User.findById('001514527699550000')
	print(user)
	'''
	user = User(name = 'qpf', password = '123123', email = 'qpf0510@qq.com', admin = '0', image = '../res/tumblr.png')
	print(user.save())
	'''
	
	
