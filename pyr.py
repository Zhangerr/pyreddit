#!/usr/bin/python
#add unit tests? 
import requests
import pdb
import HTMLParser
client = requests.session()
headers={'User-Agent':'akun bot'}
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
	return client.post(url,data=data,headers=headers) # make sure to use named args)

class Link(AttributeDict): # http://stackoverflow.com/questions/4984647/accessing-dict-keys-like-an-attribute-in-python attribute dictionary
	def __init__(self,*args,**kwargs):
		super(Link,self).__init__(*args,**kwargs)
		self.comments = []

	def getComments(self):
		if len(self.comments) == 0:
			js = client.get("http://reddit.com" + self['permalink'] + ".json").json()
			parse = HTMLParser.HTMLParser()
			for i in js[1]['data']['children']:	
				i['data']['body_html'] = parse.unescape(i['data']['body_html'])
				self.comments.append(Comment(i['data']))
		return self.comments
		
class Comment(AttributeDict):	
	pass

class Subreddit:
	def __init__(self, name, sort):		
		self.links = []
		self.name = name
		self.sort = sort
			#links.append(Link(data['author'],data['title'],data['url'],data['name']))
	def getLinks(self):
		if len(self.links) == 0:
			js = client.get("http://reddit.com/r/" + self.name + "/"  + self.sort + "/.json").json() 		
			for i in js['data']['children']:
				data = i['data']
				self.links.append(Link(data))
		return self.links
"""class Link:
	def __init__(self,author,title,url,id):
		self.author = author
		self.url = url
		self.id = id
		self.title = title
	def comment(self,text):		
		data = {'thing_id': thread,'text':text,'uh':modhash}
		r=post('http://www.reddit.com/api/comment',data,)
		print r.json()
"""		
#class Comment:
#	def __init__(self,author,id,text):
#		self.author = author
#		self.id = id
#		self.text = text
class Reddit:			
	def login(self,u,p):
		global modhash # needed to modify it, not needed to read
		self.user = u
		self.pwd = p		
		data = {'user':u,'passwd':p,'api_type':'json'}
		r=post('https://ssl.reddit.com/api/login',data)
		modhash = r.json()['json']['data']['modhash']
		print modhash
	
	def getSubreddit(self,name, sort="hot"):
		return Subreddit(name,sort)

		
