#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
import datetime
from dbconnect import connection
import gc

def delete_existingT(company):
    c, conn = connection()

    conn.set_character_set('utf8')
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')
    c.execute("set session sql_mode='';")
    conn.commit()

    # first delete existing
    data = c.execute("delete from twitter where company = (%s)", [company])
    conn.commit()
    c.close()
    conn.close()
    gc.collect()
    return data

def db_insert(company, data, branch):

    c, conn = connection()

    conn.set_character_set('utf8')
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')
    c.execute("set session sql_mode='';")
    conn.commit()

    # then insert new
    created = ''
    text = ''
    post_type = ''
    favorites = None
    retweets = None
    retweeted = None
    inreplytouser = ''


    try:
        if data[1] and data[1].strip() is not '':
            created = data[1]
    except IndexError as e:
        print e

    try:
        if data[3] and data[3].strip() is not '':
            text = data[3]
    except IndexError as e:
        print e

    try:
        if data[7] and data[7].strip() is not '':
            post_type = data[7]
    except IndexError as e:
        print e

    try:
        if data[4] and data[4].strip() is not '':
            favorites = data[4]
    except IndexError as e:
        print e

    try:
        if data[5] and data[5].strip() is not '':
            retweets = data[5]
    except IndexError as e:
        print e

    try:
        if data[6] and data[6].strip() is not '':
            if data[6].strip() is 'False':
                retweeted = 0
            elif data[6].strip() is 'True':
                retweeted = 1
    except IndexError as e:
        print e

    try:
        if data[8] and data[8].strip() is not '' and data[8].strip() is not 'None':
            inreplytouser = data[8]
    except IndexError as e:
        print e
        
    query = "insert into twitter (company, created, text, type, favorites, retweets, retweeted, inreplytouser, branch_id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

    c.execute(query, (company, created, text.encode('utf-8'), post_type, favorites, retweets, retweeted, inreplytouser, branch))

    conn.commit()

    c.close()
    conn.close()
    gc.collect()


# credentials from https://apps.twitter.com/
consumerKey = "xxxxxxxxxxxxxxxxxxxxxxxxx"
consumerSecret = "yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"
accessToken = "zzzzzzzz-wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww"
accessTokenSecret = "vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv"



def TwitterParser(screen_name, since, until, delete, branch):
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, monitor_rate_limit=True)

    username = screen_name

    if delete==1:
        delete_existingT(username)

    startDate = datetime.datetime.strptime(since, '%d/%m/%Y').strftime('%Y-%m-%d')
    startDate = datetime.datetime.strptime(startDate, '%Y-%m-%d')
    endDate = datetime.datetime.strptime(until, '%d/%m/%Y').strftime('%Y-%m-%d')
    endDate = datetime.datetime.strptime(endDate, '%Y-%m-%d')

    tweets = []
    tmpTweets = api.user_timeline(username)
    for tweet in tmpTweets:
        if tweet.created_at < endDate and tweet.created_at > startDate:
            tweets.append(tweet)

    # while (tmpTweets[-1].created_at > startDate):
    while (tmpTweets and tmpTweets[-1].created_at > startDate):
        print("Last Tweet @", tmpTweets[-1].created_at, " - fetching some more")
        tmpTweets = api.user_timeline(screen_name = username, max_id = tmpTweets[-1].id, exclude_replies=0, include_rts=1)
        for tweet in tmpTweets:
            if tweet.created_at < endDate and tweet.created_at > startDate:
                tweets.append(tweet)

    ttype = ''
    outtweets = []

    for tweet in tweets:
        if tweet.entities.get('media') and 'type' in tweet.entities.get('media')[0]:
            ttype = tweet.entities.get('media')[0]['type']
        else:
            if tweet.text and 'http' in tweet.text:
                ttype='link'
            else:
                ttype='text'

        twt = [str(tweet.id), str(tweet.created_at), str(tweet.created_at).split(' ')[1],
            tweet.text.replace('\n', ' ').replace('"', '').replace('&amp;', '&'),
            str(tweet.favorite_count), str(tweet.retweet_count), str(tweet.retweeted),
            str(ttype), str(tweet.in_reply_to_user_id)
            ]

        outtweets.extend([twt])

        db_insert(username, twt, branch)

    return outtweets
