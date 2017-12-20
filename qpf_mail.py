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
from email.header import Header
from email.utils import parseaddr, formataddr

import smtplib

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
	
	server = smtplib.SMTP(smtp_server, port)
	server.starttls()
	server.set_debuglevel(1)
	server.login(send_addr, passwd)
	server.sendmail(send_addr, [recv_addr], msg.as_string())
	server.quit()

if __name__ == '__main__':
	print(__doc__  % __author__)
	email_send('qpf0510@qq.com', 'pwhzvfvkapncbfib', 'qpf0510@qq.com', 'smtp.qq.com', 587)
	
	
