#!/usr/bin/python3
#-*- coding: utf-8 -*-
'''
	***************
	* Web       *
	***************
	powered by %s
'''

__author__ = 'Shadaileng'

from com.qpf.qpf_log import log_time_data
from wsgiref.simple_server import make_server
from flask import Flask, request, render_template

def appication(environ, respond):
	respond('200 ok', [('Content-Type', 'text/html')])
	body = '<h1>Hello Web %s</h1>' % ('I\'m %s' % environ['LOGNAME'] or '...')
	return [body.encode('utf-8')]

def wsgi():
	server = make_server('', 8080, appication)
	log_time_data('Http listening on port 8080 ...')
	server.serve_forever()
	
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def home():
	return '<h1>Home Page</h1><a href="/login">login</a>'

@app.route('/login', methods=['GET'])
def login_form():
	return '''
			<form action="/login" method="post">
				name: <input name="name"><br/>
				passwd: <input name="passwd"><br/>
				<button type="submit">Login</button>
			</form>
			'''

@app.route('/login', methods=['POST'])
def login():
	if request.form['name'] == 'admin' and request.form['passwd'] == 'admin':
		return '<h3>Login Success</h3>'
	else:
		return '<h3>bad name or passwd</h3>'

@app.route('/template', methods = ['GET', 'POST'])
def home_template():
	return render_template('home.html')
	
@app.route('/login/template', methods=['GET'])
def form_template():
	return render_template('form.html')
	
@app.route('/logout/template', methods=['GET'])
def logout():
	return render_template('home.html')

@app.route('/login/template', methods=['POST'])
def login_template():
	name = request.form['name']
	passwd = request.form['passwd']
	
	if name == 'admin' and passwd == 'admin':
		return render_template('home.html', name = name)
	if name != 'admin':
		return render_template('form.html', message = 'wrong name', name = name)
	if passwd != 'admin':
		return render_template('form.html', message = 'wrong password', name = name)
if __name__ == '__main__':
	print(__doc__  % __author__)
#	wsgi()

	app.run()

