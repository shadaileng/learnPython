#!/usr/bin/python3
#-*- coding: utf-8 -*-
'''
	***************
	* Email	     *
	***************
	powered by %s
'''

__author__ = 'Shadaileng'

from com.qpf.qpf_log import log_time_data

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

from email import encoders
from email.header import Header, decode_header
from email.parser import Parser
from email.utils import parseaddr, formataddr

import smtplib, poplib

def _format_addr(s):
	name, addr = parseaddr(s)
	return formataddr((Header(name, 'utf-8').encode(), addr))

def email_send(send_addr, passwd, recv_addr, smtp_server, port):
	log_time_data('confirm send_addr: %s' % send_addr)
	log_time_data('confirm passwd: %s' % passwd)
	log_time_data('confirm recv_addr: %s' % recv_addr)
	log_time_data('confirm smtp_server: %s' % smtp_server)
	log_time_data('confirm port: %s' % port)
	
	msg = MIMEMultipart()
	msg['From'] = _format_addr('Sender<%s>' % send_addr)
	msg['To'] = _format_addr('Recever<%s>' % recv_addr)
	msg['Subject'] = Header('Python send Email', 'utf-8').encode()
	
	msgText = MIMEText('Send From Python... (text)', 'plain', 'utf-8')
	msg.attach(msgText)
	
	msgHtml = MIMEText('<html><body><h1>Python</h1><p>Send From Python... (HTML)<img src="cid:0"></p></body></html>', 'html', 'utf-8')
	msg.attach(msgHtml)
	
	with open('./res/zf.jpeg', 'rb') as f:
		mime = MIMEBase('image', 'jpeg', filename='zf.jpeg')
		mime.add_header('Content-Disposition', 'attachment', filename='zf.jpeg')
		mime.add_header('Content-ID', '<0>')
		mime.add_header('X-Attachment-Id', '0')
		
		mime.set_payload(f.read())
		encoders.encode_base64(mime)
		msg.attach(mime)
	
	server = smtplib.SMTP(smtp_server, port)
	server.starttls()
	server.set_debuglevel(1)
	server.login(send_addr, passwd)
	server.sendmail(send_addr, [recv_addr], msg.as_string())
	server.quit()
	
def _decode_header(s):
	val, charset = decode_header(s)[0]
	if charset:
		val = val.decode(charset)
	return val
	
def guess_charset(msg):
	charset = msg.get_charset()
	if charset is None:
		content_type = msg.get('Content-Type', '').lower()
		pos = content_type.find('charset=')
		if pos >= 0:
			charset = content_type[pos + 8 : ].strip()
	return charset
	
def print_info(msg, indent=0):
	if indent == 0:
		for header in ['From', 'To', 'Subject']:
			val = msg.get(header, '')
			if val:
				if header == 'Subject':
					val = _decode_header(val)
				else:
					hddr, addr = parseaddr(val)
					name = _decode_header(hddr)
					val = '%s <%s>' % (name, addr)
			print('%s%s: %s' % ('' * indent, header, val))
	if msg.is_multipart():
		parts = msg.get_payload()
		for n, part in enumerate(parts):
			print('%spart: %s' % (' ' * indent, n))
			print('%s------------------------------------' % (' ' * indent))
			print_info(part, indent + 1)
	else:
		content_type = msg.get_content_type()
		if content_type == 'text/plain' or content_type == 'text/html':
			content = msg.get_payload(decode = True)
			charset = guess_charset(msg)
			if charset:
				content = content.decode(charset)
			print('%sText: %s' % (' ' * indent, content + '...'))
		else:
			print('%sAttachmentL %s' % (' ' * indent, content_type))
	print('%s------------------------------------' % (' ' * indent))
def email_recv(addr, passwd, pop3_server, port):
	server = poplib.POP3_SSL(pop3_server, port)
	server.set_debuglevel(1)
	print(server.getwelcome().decode('utf-8'))
	
	server.user(addr)
	server.pass_(passwd)
	
	print('Message: %s, Size: %s' % server.stat())
	
	resp, mails, octets = server.list()
	print(mails)
	
	index = len(mails)
	
	resp, lines, octets = server.retr(index)
	
	msg_content = b'\r\n'.join(lines).decode('utf-8')
	
	msg = Parser().parsestr(msg_content)
	
	print_info(msg)
	
	server.quit()
	
if __name__ == '__main__':
	print(__doc__  % __author__)
#	email_send('qpf0510@qq.com', 'pwhzvfvkapncbfib', 'qpf0510@qq.com', 'smtp.qq.com', 25)
	email_recv('qpf0510@qq.com', 'pwhzvfvkapncbfib', 'pop.qq.com', 995)
	
