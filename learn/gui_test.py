#!/usr/bin/python3
#-*- coding: utf-8 -*-
'''
	*************************
	* GUI module *
	*************************
	powered by %s
'''

__author__ = 'Shadaileng'

'''
	需要安装tkinter的模块
	sudo pacman -S python-pmw
'''
from tkinter import *
import tkinter.messagebox as messagebox

class Application(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.pack()
		self.createWidgets()
	def createWidgets(self):
		self.nameinput = Entry(self)
		self.nameinput.pack()
		self.sayhello = Button(self, text='Hello', command=self.hello)
		self.sayhello.pack()
	def hello(self):
		name = self.nameinput.get() or 'World'
		messagebox.showinfo('Message', 'Hello %s' % name)
	
if __name__ == '__main__':
	app = Application()
	app.master.title('Hello World')
	app.mainloop()
