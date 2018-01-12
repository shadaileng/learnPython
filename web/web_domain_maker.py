#!/usr/bin/python3
#-*- coding: utf-8 -*-
'''
	**********************
	* domain maker     *
	**********************
	powered by %s
'''

__author__ = 'Shadaileng'

import logging; logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(filename)s line:%(lineno)d %(message)s')
import asyncio
from web_db import select, execute

class Field(object):
	def __init__(self, name, column_type, primary_key, default):
		self.name = name
		self.column_type = column_type
		self.primary_key = primary_key
		self.default = default
	def __str__(self):
		return '<%s, %s: %s>' % (self.__class__.__name__, self.column_type, self.name)

class StringField(Field):
	def __init__(self, name = None, column_type = 'varchar(100)', primary_key = False, default = None):
		super().__init__(name, column_type, primary_key, default)

class NumberField(Field):
	def __init__(self, name = None, column_type = 'Number(10)', primary_key = False, default = None):
		super().__init__(name, column_type, primary_key, default)

class ModelMetaClass(type):
	def __new__(cls, name, base, attrs):
		if name == 'Model':
			return type.__new__(cls, name, base, attrs)
		logging.info('Found model %s' % name)
		
		mappings = dict()
		primary_key = None
		for k, v in attrs.items():
			if isinstance(v, Field):
				logging.info('Found mapping: %s ==> %s' % (k, v))
				mappings[k] = v
				if v.primary_key:
					if primary_key:
						raise RuntimeError('primary_key is not unique')
					else:
						primary_key = k
		for k in mappings.keys():
			attrs.pop(k)
		attrs['__primary_key__'] = primary_key
		attrs['__fields__'] = mappings.keys()
		attrs['__mappings__'] = mappings
		attrs['__table__'] = name
		return type.__new__(cls, name, base, attrs)
class Model(dict, metaclass=ModelMetaClass):
	def __init__(self, **kw):
		super(Model, self).__init__(**kw)
	def __getattr__(self, key):
		try:
			return self[key]
		except KeyError:
			raise AttributeError('Model Object has no attribute %s' % key)
	def __setattr__(self, key, values):
		self[key] = values
	def getvalue(self, key):
		return getattr(self, key, None)
	def getValueOrDefault(self, key):
		value = getattr(self, key, None)
		if value is None:
			field = self.__mappings__[key]
			if field.default is not None:
				value = field.default() if callable(field.default) else field.default
				logging.info('field %s using default value %s' % (key, str(value)))
				setattr(self, key, value)
		return value
		
	def rows2mapping(self, rows):
		d = []
		fields = list(self.__fields__)
		for row in rows:
			r = {}
			for i in range(len(fields)):
				r[fields[i]] = row[i]
			d.append(r)
		return d
	@asyncio.coroutine
	def save(self):
		params = []
		args = []
		for k, v in self.__mappings__.items():
			params.append('?')
			args.append(self.getValueOrDefault(k)) 
		sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(self.__fields__), ','.join(params))
		logging.info('SQL: %s' % sql)
		logging.info('ARGS: %s' % args)
		return execute(sql, args)
	@asyncio.coroutine
	def delete(self):
		params = []
		args = []
		for k, v in self.__mappings__.items():
			if not getattr(self, k, None):
				continue
			params.append('%s = ?' % k)
			args.append(self.getValueOrDefault(k)) 
		sql = 'delete from %s where %s' % (self.__table__, ','.join(params))
		logging.info('SQL: %s' % sql)
		logging.info('ARGS: %s' % args)
		return execute(sql, args)
	@asyncio.coroutine
	def update(self):
		params = []
		args = []
		for k, v in self.__mappings__.items():
			if k == self.__primary_key__ or v is None:
				continue
			params.append('%s = ?' % k)
			args.append(self.getvalue(k))
		args.append(self.getvalue(self.__primary_key__))
		sql = 'update %s set %s where %s = ?' % (self.__table__, ','.join(params), self.__primary_key__)
		logging.info('SQL: %s' % sql)
		logging.info('id: %s' % self.getValueOrDefault(self.__primary_key__))
		return execute(sql, args)
	@asyncio.coroutine
	def find(self, size = None):
		params = ['1 = 1']
		args = []
		for k, v in self.__mappings__.items():
			if not self.getvalue(k):
				continue
			params.append('%s = ?' % k)
			args.append(self.getvalue(k)) 
		sql = 'select %s from %s where %s' % (','.join(self.__fields__), self.__table__, ' and '.join(params))
		logging.info('SQL: %s' % sql)
		logging.info('ARGS: %s' % args)
		rows = self.rows2mapping(select(sql, args, size))
		if len(rows) <= 0:
			return None
		return [Model(**row) for row in rows]
	@asyncio.coroutine
	@classmethod
	def deleteById(self, id):
		sql = 'delete from %s where %s = ?' % (self.__table__, self.__primary_key__)
		logging.info('SQL: %s' % sql)
		logging.info('id: %s' % id)
		return execute(sql, [id])
	@asyncio.coroutine
	def findById(self, id):
		sql = 'select %s from %s where %s = ?' % (','.join(self.__fields__), self.__table__, self.__primary_key__)
		logging.info('SQL: %s' % sql)
		logging.info('id: %s' % id)
		rows = self.rows2mapping(self, select(sql, [id], 1))
		return self(**rows[0]) 

if __name__ == '__main__':
	print(__doc__ % __author__)
	class User(Model):
		id = NumberField('id', primary_key = True)
		name = StringField('name')
		password = StringField('password')
	'''
	user = User(id = 111, name = 'Shadaileng', password = '123123')
	user.save()
	user.update()
	user1 = User(id = 111, name = 'Shadaileng')
	user1.find()
	user1.delete()
	User.findById(3)
	User.deleteById(3)
	'''
	'''
	rs = User(id = 3).find()
	for row in rs:
		logging.info(row)
	rs = User.findById(1)
	for row in rs:
		logging.info(row)
	rs = User(id = 3, name = 'Chik Shadaileng', password = '89509').update()
	rs = User(id = 4, name = 'Chik Shadaileng', password = '89509').save()
	logging.info(rs)
	'''
	rs = User().find()
	for row in rs:
		logging.info(row)
		
	
