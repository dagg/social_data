# -*- coding: utf-8 -*-

from dbconnect import connection
import gc
import datetime

from get_fbacebook_followers import FB_Followers_parser

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def get_fb_data(company, since, until):

	c, conn = connection()

	conn.set_character_set('utf8')
	c.execute('SET NAMES utf8;')
	c.execute('SET CHARACTER SET utf8;')
	c.execute('SET character_set_connection=utf8;')
	c.execute("set session sql_mode='';")
	conn.commit()

	# first delete existing
	if since and until and str(since).strip()!='' and str(until).strip()!='':
		since = datetime.datetime.strptime(since, '%d/%m/%Y').strftime('%Y-%m-%d')
		until = datetime.datetime.strptime(until, '%d/%m/%Y').strftime('%Y-%m-%d')
		res = c.execute("select facebook.id, company, company_name, created, message, char_length(message) as message_chars, type, likes, shares, comments from facebook where  message != '' and company= (%s) and created>=Date((%s)) and created<DATE_ADD(DATE((%s)), INTERVAL 1 DAY) ", [company, since, until])
	else:
		res = c.execute("select facebook.id, company, company_name, created, message, char_length(message) as message_chars, type, likes, shares, comments from facebook where  message != '' and company= (%s)", [company])
	data = list(c.fetchall())
	conn.commit()
	c.close()
	conn.close()
	gc.collect()
	return data, company, FB_Followers_parser(company), get_company_branch('facebook', company)

def get_twitter_data(company, since, until):

	c, conn = connection()

	conn.set_character_set('utf8')
	c.execute('SET NAMES utf8;')
	c.execute('SET CHARACTER SET utf8;')
	c.execute('SET character_set_connection=utf8;')
	c.execute("set session sql_mode='';")
	conn.commit()

	if since and until and str(since).strip()!='' and str(until).strip()!='':
		since = datetime.datetime.strptime(since, '%d/%m/%Y').strftime('%Y-%m-%d')
		until = datetime.datetime.strptime(until, '%d/%m/%Y').strftime('%Y-%m-%d')
		res = c.execute("select twitter.id, company, created, text, char_length(text) as text_chars, type, favorites, retweets, retweeted, inreplytouser from twitter where company= (%s) and created>=Date((%s)) and created<DATE_ADD(DATE((%s)), INTERVAL 1 DAY)", [company, since, until])
	else:
		res = c.execute("select twitter.id, company, created, text, char_length(text) as text_chars, type, favorites, retweets, retweeted, inreplytouser from twitter where company= (%s)", [company])
	data = list(c.fetchall())
	conn.commit()
	c.close()
	conn.close()
	gc.collect()
	return data, company, get_company_branch('twitter', company)


def get_googleplus_data(company, since, until):
	
	c, conn = connection()

	conn.set_character_set('utf8')
	c.execute('SET NAMES utf8;')
	c.execute('SET CHARACTER SET utf8;')
	c.execute('SET character_set_connection=utf8;')
	c.execute("set session sql_mode='';")
	conn.commit()

	if since and until and str(since).strip()!='' and str(until).strip()!='':
		since = datetime.datetime.strptime(since, '%d/%m/%Y').strftime('%Y-%m-%d')
		until = datetime.datetime.strptime(until, '%d/%m/%Y').strftime('%Y-%m-%d')
		res = c.execute("select googleplus.id, company, company_code, created, googleplus.name, char_length(googleplus.name) as name_chars, content, char_length(content) as content_chars, type, comments, likes, shares from googleplus where company= (%s) and created>=Date((%s)) and created<DATE_ADD(DATE((%s)), INTERVAL 1 DAY)", [company, since, until])
	else:
		res = c.execute("select googleplus.id, company, company_code, created, googleplus.name, char_length(googleplus.name) as name_chars, content, char_length(content) as content_chars, type, comments, likes, shares from googleplus where company= (%s)", [company])

	data = list(c.fetchall())



	conn.commit()
	c.close()
	conn.close()
	gc.collect()
	return data, company, get_company_branch('googleplus', company)


def get_branches():
	
	c, conn = connection()

	conn.set_character_set('utf8')
	c.execute('SET NAMES utf8;')
	c.execute('SET CHARACTER SET utf8;')
	c.execute('SET character_set_connection=utf8;')
	c.execute("set session sql_mode='';")
	conn.commit()

	res = c.execute("select id, name from branches")
	data = list(c.fetchall())
	conn.commit()
	c.close()
	conn.close()
	gc.collect()
	return data


def get_company_branch(social, company):
	
	c, conn = connection()

	conn.set_character_set('utf8')
	c.execute('SET NAMES utf8;')
	c.execute('SET CHARACTER SET utf8;')
	c.execute('SET character_set_connection=utf8;')
	c.execute("set session sql_mode='';")
	conn.commit()

	res = c.execute("select branches.id, branches.name from {0}, branches where {0}.branch_id=branches.id and company='{1}'".format(social, company))
	data = list(c.fetchall())
	conn.commit()
	c.close()
	conn.close()
	gc.collect()
	return data