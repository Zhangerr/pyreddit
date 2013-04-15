#!/usr/bin/python
#add unit tests? 
#consider splitting into multiple files based on class-- use import config trick for globals

import requests
import pdb
import HTMLParser
client = requests.session()
headers={}
modhash = ''
def isloggedin():
	if len(modhash) == 0:
		print "you must be logged in to use this function"
		return False
	return True
class AttributeDict(dict):
 	def vote(self,dir):
		if isloggedin():
			data = {'thing_id':self.name,'uh':modhash,'dir':dir}
			r=post('http://www.reddit.com/api/comment',data)
			print r.json()
	def comment(self,text):
		if isloggedin():
			data = {'thing_id': self.name,'text':text,'uh':modhash}
			r=post('http://www.reddit.com/api/comment',data)
			print r.json()	
	def __getattr__(self, attr):
		return self[attr]
	def __setattr__(self, attr, value):
		self[attr] = value

def post(url,data):
	return client.post(url,data=data,headers=headers) # make sure to use named args

class Link(AttributeDict): # http://stackoverflow.com/questions/4984647/accessing-dict-keys-like-an-attribute-in-python attribute dictionary
	def __init__(self,unescaped = True,*args,**kwargs):
		super(Link,self).__init__(*args,**kwargs)
		self.comments = []
		js = client.get("http://reddit.com" + self['permalink'] + ".json").json()
		parse = HTMLParser.HTMLParser()
		for i in js[1]['data']['children']:	
			if unescaped:
				i['data']['body_html'] = parse.unescape(i['data']['body_html'])
			self.comments.append(Comment(i['data']))
	def __repr__(self):
		return "link: %s" % self.title
		
	def getComments(self):
		return self.comments
		
class Comment(AttributeDict):	
	def __repr__(self):
		return 'comment' #todo, add parent link or comment content

class Subreddit:
	def __init__(self, name, sort):				
		self.name = name
		self.sort = sort			
		self.refresh()
	def getLinks(self):
		return self.links

	#should both return new subreddit objects or modify the current? add pages object?	
	def getNextPage(self):
		pass
	def getPrevPage(self):
		pass
	def __repr__(self):
		return "subreddit: %s" % self.name		
	def refresh(self):
		self.links = []
		js = client.get("http://reddit.com/r/%s/%s/.json" % (self.name,self.sort)).json() 		
		self.after = js['data']['after']
		self.before = js['data']['before']
		for i in js['data']['children']:
			data = i['data']
			#print data
			self.links.append(Link(True,data))		
#note to self, perhaps make generators instead of lists for results, could be more efficient, that is, function with yield
class Reddit:			
	def __init__(self,ua="default"):
		global headers
		headers={'User-Agent':ua}
	def login(self,u,p):
		global modhash # needed to modify it, not needed to read
		self.user = u
		self.pwd = p		
		data = {'user':u,'passwd':p,'api_type':'json'}
		r=post('https://ssl.reddit.com/api/login',data)
		modhash = r.json()['json']['data']['modhash']
		print modhash
	def getRandom(self):
		pass
	def getSubreddit(self,name, sort="hot"):
		return Subreddit(name,sort)