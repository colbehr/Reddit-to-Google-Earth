from fake_useragent import UserAgent
import time
import praw
import os
import re
from geopy.geocoders import Bing
import json
import simplekml
kml = simplekml.Kml()

#https://www.reddit.com/prefs/apps/
prawId= ""
prawSecret = ""
#https://www.bingmapsportal.com/Application
BingApiKey = ""

#Subreddits to search
subs = ["EarthPorn","AbandonedPorn"]
#Text to search in each subreddit
searchTerm = "Washington OR Wa"
#Number of posts to get from each sub
postNumber = 10


def userAgent():
    ua = UserAgent()
    return ua.random

#returns Array of Posts [title, url]
def getPosts(sub,num):
	postText = []
	r = praw.Reddit(client_id=prawId, client_secret=prawSecret, user_agent=userAgent())
	r.read_only = True
	print("Getting posts from "+str(sub))
	posts = r.subreddit(sub).search(searchTerm, limit=num)
	for x in posts:
		postText.append([x.title, x.url])
	return postText


for sub in subs:
	Loclist = getPosts(sub,postNumber)
	geolocator = Bing(BingApiKey)
	for loc in Loclist:
		loc[0] = re.sub("[\(\[].*?[\)\]]", "", loc[0]).strip()
		print(loc)
		location = geolocator.geocode(loc)
		if(location is not None):
			loc.append((location.latitude, location.longitude))
			print((location.latitude, location.longitude))
			kml.newpoint(name=loc[0], description=loc[1], coords=[(loc[2][1],loc[2][0])])
		time.sleep(.5)
	print(json.dumps(Loclist,sort_keys=True, indent=4, separators=(',', ': ')))
	kml.save(sub+".kml")