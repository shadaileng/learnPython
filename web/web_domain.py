#!/usr/bin/python3
#-*- coding: utf-8 -*-
'''
	****************
	* domain     *
	****************
	powered by %s
'''

__author__ = 'Shadaileng'

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

class IntegerField(Field):
	def __init__(self, name = None, column_type = 'Number(10)', primary_key = False, default = None):
		super().__init__(name, column_type, primary_key, default)

class ModelMetaClass(type):
	def __new__(cls, name, base, attrs):
		if name == 'Model':
			return type.__new__(cls, name, base, attrs)
		print('Found model %s' % name)
		
		mappings = dict()
		primary_key = None
		for k, v in attrs.items():
			if isinstance(v, Field):
				print('Found mapping: %s ==> %s' % (k, v))
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
	def save(self):
		params = []
		args = []
		for k, v in self.__mappings__.items():
			params.append('?')
			args.append(getattr(self, k, None)) 
		sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(self.__fields__), ','.join(params))
		print('SQL: %s' % sql)
		print('ARGS: %s' % args)
	def update(self):
		params = []
		args = []
		for k, v in self.__mappings__.items():
			if k == self.__primary_key__:
				continue
			params.append('%s = ?' % k)
			args.append(getattr(self, k, None)) 
		sql = 'update %s set %s where %s = ?' % (self.__table__, ','.join(params), self.__primary_key__)
		print('SQL: %s' % sql)
		print('id: %s' % getattr(self, self.__primary_key__, None))
	@classmethod
	def find(self, id):
		sql = 'select %s from %s where %s = "%s"' % (','.join(self.__fields__), self.__table__, self.__primary_key__, '?')
		print('SQL: %s' % sql)
		print('id: %s' % id)
class User(Model):
	id = IntegerField('id', primary_key = True)
	name = StringField('name')
	password = StringField('password')

if __name__ == '__main__':
	print(__doc__ % __author__)
	user = User(id = 111, name = 'Shadaileng', password = '123123')
	user.save()
	user.update()
	User.find(3)
