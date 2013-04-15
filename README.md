pyreddit
========

my own spin on the reddit api in python (just practice), I don't think it'll ever be anywhere close to PRAW

**YOU MUST HAVE THE PYTHON PACKAGE [REQUESTS](http://docs.python-requests.org/en/latest/) TO USE THIS LIBRARY**

initialize the api by creating a new Reddit object:
```python
from pyr import Reddit
r = Reddit()
```
if you want to comment or vote on anything, you will have to login with a user:
```python
r.login("youruser","yourpass")
```
you can select a subreddit which you want to manipulate, optionally specifying the sorting order (defaults to "hot"):
```python
sr = r.getSubreddit("askscience","new")
```
*NOTE: everytime you call getSubreddit a new object is created and thus when you call getLinks() on that subreddit it re-downloads data from the web, so if you want to store the state of the subreddit assign it to a variable*

you can then get all the front page links with getLinks (note that only the first page is supported for now)
```python
links = sr.getLinks()
```
the links are just a regular list, so you can use functions like filter, reduce, map, etc. Each link contains the following attributes:
```
domain: "self.askscience",
banned_by: null,
media_embed: { },
subreddit: "askscience",
selftext_html: null,
selftext: "",
likes: null,
link_flair_text: null,
id: "1c8ovk",
clicked: false,
title: "Why does it hurt when I bite aluminum foil?",
media: null,
score: 24,
approved_by: null,
over_18: false,
hidden: false,
thumbnail: "",
subreddit_id: "t5_2qm4e",
edited: false,
link_flair_css_class: null,
author_flair_css_class: null,
downs: 7,
saved: false,
is_self: true,
permalink: "/r/askscience/comments/1c8ovk/why_does_it_hurt_when_i_bite_aluminum_foil/",
name: "t3_1c8ovk",
created: 1365840204,
url: "http://www.reddit.com/r/askscience/comments/1c8ovk/why_does_it_hurt_when_i_bite_aluminum_foil/",
author_flair_text: null,
author: "Logical_Primate",
created_utc: 1365811404,
ups: 31,
num_comments: 2,
num_reports: null,
distinguished: null
```
which you can access either with foo['name'] or foo.name.
You can comment or vote on the article with corresponding method:
```python
links[0].comment("hello")
links[0].vote("1") #1 for upvote, -1 for downvote, 0 to undo the vote
```
You can view the comments on the article with the getComments method:
```python
com = links[0].getComments()
```
As with links, you can comment on (reply to) or vote on comments as well using the same methods.

Examples
-------
filter posts in askscience that have over 700 upvotes and then comment on the first one that does so

```python
from pyr import Reddit
r = Reddit()
r.login("youruser","yourpass")
#every time getSubreddit is called the links are refreshed
links = r.getSubreddit("askscience").getLinks()
filtered = filter(lambda x:x.ups>=700,links)
if len(filtered) > 0:
  filtered[0].comment("testing 123")
```
