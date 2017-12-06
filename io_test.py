#!/usr/bin/python3
#-*- coding: utf-8 -*-

from com.qpf.domain import Person
import pickle
import json

def person2dict(person):
	return {
		'name': person.name,
		'age': person.age,
		}
def dict2person(d):
	return Person(d['name'], d['age'])
def picking():
	print('*******pickle***********')
	
	d = dict(name = 'Shadaileng', age = 25)
	
	print(pickle.dumps(d))
	
	f = open('./dump.tmp', 'wb')
	
	pickle.dump(d, f)
	
	f.close()
	
	print(pickle.loads(pickle.dumps(d)))
	
	f = open('./dump.tmp', 'rb')
	
	print(pickle.load(f))
	
	f.close()
	
	print('*******json***********')
	jsonStr = json.dumps(d)
	print(jsonStr)
	d_ = json.loads(jsonStr)
	print(d_)
	
	shadaileng = Person('shadaileng', 25)
	jsonStr = json.dumps(shadaileng, default=person2dict)
	print(jsonStr)
	person = json.loads(jsonStr, object_hook=dict2person)
	print(person)
