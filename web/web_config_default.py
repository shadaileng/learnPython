#!/usr/bin/python3
#-*- coding: utf-8 -*-

'''
	************************
	*   Default Config  *
	************************
	     Powered By %s
'''

__author__ = 'SHadaileng'

class Dict(dict):
	def __init__(self, names = (), values = (), **kw):
		super(Dict, self).__init__(**kw)
		for k, v in zip(names, values):
			self[k] = v
	def __getattr__(self, key):
		try:
			return self[key]
		except KeyError:
			raise AttributeError(r"'Dict' object has no attribute %s" % key)
		
	def __setattr__(self, key, val):
		self[key] = val

def merge(defaults, override):
	r = {}
	for k, v, in defaults.items():
		if k in override:
			if isinstance(v, dict):
				r[k] = merge(v, override[k])
			else:
				r[k] = override[k]
		else:
			r[k] = v
	return r

def toDict(d):
	D = Dict()
	for k, v in d.items():
		D[k] = toDict(v) if isinstance(v, dict) else v
	return D

configs = {
	'debug': True,
	'db': 'test.db'
}

try:
	import web_config_override
	configs = merge(configs, web_config_override.configs)
except ImportError:
	pass
	
configs = toDict(configs)

if __name__ == '__main__':
	print(__doc__ % __author__)
	
	print(configs)
