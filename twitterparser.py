#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv
from datetime import datetime
from dateutil import tz

from_zone = tz.gettz('UTC')
to_zone = tz.gettz('Europe/Athens')

#Twitter API credentials
consumer_key = "xxxxxxxxxxxxxxxxxxxxxxxxx"
consumer_secret = "yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"
access_key = "zzzzzzzz-wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww"
access_secret = "vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv"


def date_fix(datetime):
	day=str(datetime.day)
	month=str(datetime.month)
	year=str(datetime.year)

	if datetime.day < 10:
		day="0"+str(datetime.day)
	if datetime.month < 10:
		month="0"+str(datetime.month)

	return day+"-"+month+"-"+str(datetime.year)

def time_fix(datetime):
	hour=str(datetime.hour)
	minute=str(datetime.minute)
	second=str(datetime.second)

	if datetime.hour < 10:
		hour="0"+str(datetime.hour)
	if datetime.minute < 10:
		minute="0"+str(datetime.minute)
	if datetime.second < 10:
		second="0"+str(datetime.second)

	return hour+":"+minute+":"+second


def TwitterParser(screen_name):
# def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	# new_tweets = api.user_timeline(screen_name = screen_name,count=200, exclude_replies=1)
	# new_tweets = api.user_timeline(screen_name = screen_name,count=200, exclude_replies=1)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200, exclude_replies=0, include_rts=1)
	
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	# keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print "getting tweets before %s" % (oldest)
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest, exclude_replies=0, include_rts=1)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print "...%s tweets downloaded so far" % (len(alltweets))

	# new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
	# alltweets.extend(new_tweets)

	#transform the tweepy tweets into a 2D array that will populate the csv	
	# outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8"), tweet.favorite_count, tweet.retweet_count, tweet.retweeted] for tweet in alltweets]
	ttype = ''
	outtweets = []
	for tweet in alltweets:
		if tweet.entities.get('media') and 'type' in tweet.entities.get('media')[0]:
			ttype = tweet.entities.get('media')[0]['type']
		utc = datetime.strptime(str(tweet.created_at), '%Y-%m-%d %H:%M:%S')
		utc = utc.replace(tzinfo=from_zone)
		created_at = utc.astimezone(to_zone)
		created_at_date = date_fix(created_at)
		created_at_hour = time_fix(created_at)
		outtweets.extend([[tweet.id_str, created_at_date, created_at_hour, tweet.text.encode("utf-8").decode("utf-8").replace('\n', ' ').replace('"', '').replace('&amp;', '&'), tweet.favorite_count, tweet.retweet_count, tweet.retweeted, ttype, tweet.in_reply_to_user_id]])
		ttype = '' 

	# return ["id","created_date", "created_hour","text", "favorite_count", "retweet_count", "retweeted", "type", "in_reply_to_user_id"]
	return outtweets
