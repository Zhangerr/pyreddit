#!/usr/bin/python

import requests

class Reddit:
	headers={'User-Agent':'akun bot'}
	user = ''
	pwd = ''
	modhash = ''
	client = None
	def __init__(self,u,p):
		self.user = u
		self.pwd = p
		self.client = requests.session()
		data = {'user':u,'passwd':p,'api_type':'json'}
		r=self.client.post('https://ssl.reddit.com/api/login',data=data,headers=self.headers)
		self.modhash = r.json()['json']['data']['modhash']
		print self.modhash
	def comment(self,thread,text):
		data = {'thing_id': thread,'text':text,'uh':self.modhash}
		r=self.client.post('http://www.reddit.com/api/comment',data=data,headers=self.headers)
		print r.json()
