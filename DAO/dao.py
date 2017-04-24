# -*- coding: utf-8 -*-

from dict_dbconnect import connection
import gc
import datetime

import sys
reload(sys)
sys.setdefaultencoding("utf-8")



def get_fb_sums_per_weekdays(company, since, until, branch):

	c, conn, cdict = connection()

	conn.set_character_set('utf8')
	cdict.execute('SET NAMES utf8;')
	cdict.execute('SET CHARACTER SET utf8;')
	cdict.execute('SET character_set_connection=utf8;')
	cdict.execute("set session sql_mode='';")
	conn.commit()

	cquery=''
	bquery = ''

	if since and until and str(since).strip()!='' and str(until).strip()!='':

		if company and company != '':
			cquery = "and company = '{0}' ".format(company)
		
		if branch and branch != '':
			bquery = " and branch_id = {0} ".format(branch)

		since = datetime.datetime.strptime(since, '%d/%m/%Y').strftime('%Y-%m-%d')
		until = datetime.datetime.strptime(until, '%d/%m/%Y').strftime('%Y-%m-%d')
		query = """select company, company_name, count(*) as posts, 
					sum(likes) as likes, sum(shares) as shares, 
					sum(comments) as comments, DAYNAME(created) as weekday 
					from facebook 
					where created >= Date("{0}")
					and created < DATE_ADD(DATE('{1}'), INTERVAL 1 DAY)
					{2}
					{3}
					group by company, weekday order by company_name, FIELD(weekday, 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')""".format(since, until, cquery, bquery)
		res = cdict.execute(query)
	else:

		if company and company != '':
			cquery = "where company = '{0}' ".format(company)
			if branch and branch != '':
				bquery = " and branch_id = {0} ".format(branch)
		else:
			if branch and branch != '':
				bquery = " where branch_id = {0} ".format(branch)

		query = """select company, company_name, count(*) as posts, 
					sum(likes) as likes, sum(shares) as shares, 
					sum(comments) as comments, DAYNAME(created) as weekday 
					from facebook
					{0}
					{1}
					group by company, weekday order by company_name, FIELD(weekday, 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')""".format(cquery, bquery)
		res = cdict.execute(query)
	data = cdict.fetchall()
	conn.commit()
	cdict.close()
	conn.close()
	gc.collect()

	return data




def get_twitter_sums_per_weekdays(company, since, until, branch):

	c, conn, cdict = connection()

	conn.set_character_set('utf8')
	cdict.execute('SET NAMES utf8;')
	cdict.execute('SET CHARACTER SET utf8;')
	cdict.execute('SET character_set_connection=utf8;')
	cdict.execute("set session sql_mode='';")
	conn.commit()

	cquery=''
	bquery = ''

	if since and until and str(since).strip()!='' and str(until).strip()!='':

		if company and company != '':
			cquery = "and company = '{0}'".format(company)
		
		if branch and branch != '':
			bquery = " and branch_id = {0} ".format(branch)

		since = datetime.datetime.strptime(since, '%d/%m/%Y').strftime('%Y-%m-%d')
		until = datetime.datetime.strptime(until, '%d/%m/%Y').strftime('%Y-%m-%d')
		query = """select company, count(*) as tweets, 
					sum(favorites) as favorites, sum(retweets) as retweets,
					DAYNAME(created) as weekday 
					from twitter 
					where created >= Date("{0}")
					and created < DATE_ADD(DATE('{1}'), INTERVAL 1 DAY)
					{2}
					{3}
					group by company, weekday order by company, FIELD(weekday, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')""".format(since, until, cquery, bquery)
		res = cdict.execute(query)
	else:

		if company and company != '':
			cquery = "where company = '{0}'".format(company)
			if branch and branch != '':
				bquery = " and branch_id = {0} ".format(branch)
		else:
			if branch and branch != '':
				bquery = " where branch_id = {0} ".format(branch)

		query = """select company, count(*) as tweets, 
					sum(favorites) as favorites, sum(retweets) as retweets,
					DAYNAME(created) as weekday 
					from twitter
					{0}
					{1}
					group by company, weekday order by company, FIELD(weekday, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')""".format(cquery, bquery)
		res = cdict.execute(query)
	data = cdict.fetchall()
	conn.commit()
	cdict.close()
	conn.close()
	gc.collect()

	return data



def get_fb_sums_per_month(company, since, until, branch):

	c, conn, cdict = connection()

	conn.set_character_set('utf8')
	cdict.execute('SET NAMES utf8;')
	cdict.execute('SET CHARACTER SET utf8;')
	cdict.execute('SET character_set_connection=utf8;')
	cdict.execute("set session sql_mode='';")
	conn.commit()

	cquery=''
	bquery = ''

	if company and company != '':
		if since and until and str(since).strip()!='' and str(until).strip()!='':
			since = datetime.datetime.strptime(since, '%d/%m/%Y').strftime('%Y-%m-%d')
			until = datetime.datetime.strptime(until, '%d/%m/%Y').strftime('%Y-%m-%d')
			cquery = "and created >= Date('{0}') and created < DATE_ADD(DATE('{1}'), INTERVAL 1 DAY) ".format(since, until)

		if branch and branch != '':
			bquery = " and branch_id = {0} ".format(branch)

		query = """select MONTHNAME(created) as month, company, count(*) as posts,
					sum(likes) as likes, sum(comments) as comments,
					sum(shares) as shares
					from facebook
					where company='{0}' 
					{1}
					{2}
					group by month
					order by created, FIELD(month, 'January','February','March','April','May','June','July','August','September','October','November','December')""".format(company.strip(), cquery, bquery)
		res = cdict.execute(query)
	else:
		if since and until and str(since).strip()!='' and str(until).strip()!='':
			since = datetime.datetime.strptime(since, '%d/%m/%Y').strftime('%Y-%m-%d')
			until = datetime.datetime.strptime(until, '%d/%m/%Y').strftime('%Y-%m-%d')
			cquery = "where created >= Date('{0}') and created < DATE_ADD(DATE('{1}'), INTERVAL 1 DAY) ".format(since, until)
			if branch and branch != '':
				bquery = " and branch_id = {0} ".format(branch)
		else:
			if branch and branch != '':
				bquery = " where branch_id = {0} ".format(branch)

		query = """select MONTHNAME(created) as month, company, count(*) as posts,
					sum(likes) as likes, sum(comments) as comments,
					sum(shares) as shares
					from facebook
					{0}
					{1}
					group by month, company
					order by company, created, FIELD(month, 'January','February','March','April','May','June','July','August','September','October','November','December')""".format(cquery, bquery)
		res = cdict.execute(query)

	data = cdict.fetchall()
	conn.commit()
	cdict.close()
	conn.close()
	gc.collect()

	return data




def get_twitter_sums_per_month(company, since, until, branch):

	c, conn, cdict = connection()

	conn.set_character_set('utf8')
	cdict.execute('SET NAMES utf8;')
	cdict.execute('SET CHARACTER SET utf8;')
	cdict.execute('SET character_set_connection=utf8;')
	cdict.execute("set session sql_mode='';")
	conn.commit()

	cquery=''
	bquery = ''

	if company and company != '':
		if since and until and str(since).strip()!='' and str(until).strip()!='':
			since = datetime.datetime.strptime(since, '%d/%m/%Y').strftime('%Y-%m-%d')
			until = datetime.datetime.strptime(until, '%d/%m/%Y').strftime('%Y-%m-%d')
			cquery = "and created >= Date('{0}') and created < DATE_ADD(DATE('{1}'), INTERVAL 1 DAY) ".format(since, until)

		if branch and branch != '':
			bquery = " and branch_id = {0} ".format(branch)

		query = """select MONTHNAME(created) as month, company, count(*) as tweets,
					sum(favorites) as favorites,
					sum(retweets) as retweets
					from twitter
					where company='{0}' 
					{1}
					{2}
					group by month
					order by created, FIELD(month, 'January','February','March','April','May','June','July','August','September','October','November','December')""".format(company.strip(), cquery, bquery)
		res = cdict.execute(query)
	else:
		if since and until and str(since).strip()!='' and str(until).strip()!='':
			since = datetime.datetime.strptime(since, '%d/%m/%Y').strftime('%Y-%m-%d')
			until = datetime.datetime.strptime(until, '%d/%m/%Y').strftime('%Y-%m-%d')
			cquery = "where created >= Date('{0}') and created < DATE_ADD(DATE('{1}'), INTERVAL 1 DAY)".format(since, until)
			# cquery = "where created >= Date('{0}') and created <= '{1}'".format(since, until)
			if branch and branch != '':
				bquery = " and branch_id = {0} ".format(branch)
		else:
			if branch and branch != '':
				bquery = " where branch_id = {0} ".format(branch)

		query = """select MONTHNAME(created) as month, company, count(*) as tweets,
					sum(favorites) as favorites,
					sum(retweets) as retweets
					from twitter
					{0}
					{1}
					group by month, company
					order by company, created, FIELD(month, 'January','February','March','April','May','June','July','August','September','October','November','December')""".format(cquery, bquery)
		res = cdict.execute(query)

	data = cdict.fetchall()
	conn.commit()
	cdict.close()
	conn.close()
	gc.collect()

	return data




def get_fb_sums_per_type(company, since, until, branch):

	c, conn, cdict = connection()

	conn.set_character_set('utf8')
	cdict.execute('SET NAMES utf8;')
	cdict.execute('SET CHARACTER SET utf8;')
	cdict.execute('SET character_set_connection=utf8;')
	cdict.execute("set session sql_mode='';")
	conn.commit()

	cquery=''
	bquery = ''

	if company and company != '':
		if since and until and str(since).strip()!='' and str(until).strip()!='':
			since = datetime.datetime.strptime(since, '%d/%m/%Y').strftime('%Y-%m-%d')
			until = datetime.datetime.strptime(until, '%d/%m/%Y').strftime('%Y-%m-%d')
			cquery = "and created >= Date('{0}') and created < DATE_ADD(DATE('{1}'), INTERVAL 1 DAY) ".format(since, until)

		if branch and branch != '':
			bquery = " and branch_id = {0} ".format(branch)

		query = """select company, type, count(type) as types 
					from facebook
					where company='{0}' 
					{1}
					{2}
					group by type, company 
					order by company, type""".format(company.strip(), cquery, bquery)
		res = cdict.execute(query)
	else:
		if since and until and str(since).strip()!='' and str(until).strip()!='':
			since = datetime.datetime.strptime(since, '%d/%m/%Y').strftime('%Y-%m-%d')
			until = datetime.datetime.strptime(until, '%d/%m/%Y').strftime('%Y-%m-%d')
			cquery = "where created >= Date('{0}') and created < DATE_ADD(DATE('{1}'), INTERVAL 1 DAY) ".format(since, until)
			if branch and branch != '':
				bquery = " and branch_id = {0} ".format(branch)
		else:
			if branch and branch != '':
				bquery = " where branch_id = {0} ".format(branch)

		query = """select company, type, count(type) as types 
					from facebook
					{0}
					{1}
					group by type, company 
					order by company, type""".format(cquery, bquery)
		res = cdict.execute(query)

	data = cdict.fetchall()
	conn.commit()
	cdict.close()
	conn.close()
	gc.collect()

	return data





def get_twitter_sums_per_type(company, since, until, branch):

	c, conn, cdict = connection()

	conn.set_character_set('utf8')
	cdict.execute('SET NAMES utf8;')
	cdict.execute('SET CHARACTER SET utf8;')
	cdict.execute('SET character_set_connection=utf8;')
	cdict.execute("set session sql_mode='';")
	conn.commit()

	cquery=''
	bquery = ''

	if company and company != '':
		if since and until and str(since).strip()!='' and str(until).strip()!='':
			since = datetime.datetime.strptime(since, '%d/%m/%Y').strftime('%Y-%m-%d')
			until = datetime.datetime.strptime(until, '%d/%m/%Y').strftime('%Y-%m-%d')
			cquery = "and created >= Date('{0}') and created < DATE_ADD(DATE('{1}'), INTERVAL 1 DAY) ".format(since, until)

		if branch and branch != '':
			bquery = " and branch_id = {0} ".format(branch)

		query = """select company, type, count(type) as types 
					from twitter
					where company='{0}' 
					{1}
					{2}
					group by type, company 
					order by company, type""".format(company.strip(), cquery, bquery)
		res = cdict.execute(query)
	else:
		if since and until and str(since).strip()!='' and str(until).strip()!='':
			since = datetime.datetime.strptime(since, '%d/%m/%Y').strftime('%Y-%m-%d')
			until = datetime.datetime.strptime(until, '%d/%m/%Y').strftime('%Y-%m-%d')
			cquery = "where created >= Date('{0}') and created < DATE_ADD(DATE('{1}'), INTERVAL 1 DAY) ".format(since, until)

			if branch and branch != '':
				bquery = " and branch_id = {0} ".format(branch)
		else:
			if branch and branch != '':
				bquery = " where branch_id = {0} ".format(branch)

		query = """select company, type, count(type) as types 
					from twitter
					{0}
					{1}
					group by type, company 
					order by company, type""".format(cquery, bquery)
		res = cdict.execute(query)

	data = cdict.fetchall()
	conn.commit()
	cdict.close()
	conn.close()
	gc.collect()

	return data



def get_fb_sums_per_weekend(company, since, until, branch):

	c, conn, cdict = connection()

	conn.set_character_set('utf8')
	cdict.execute('SET NAMES utf8;')
	cdict.execute('SET CHARACTER SET utf8;')
	cdict.execute('SET character_set_connection=utf8;')
	cdict.execute("set session sql_mode='';")
	conn.commit()

	cquery=''
	bquery=''

	if company and company != '':
		if since and until and str(since).strip()!='' and str(until).strip()!='':
			since = datetime.datetime.strptime(since, '%d/%m/%Y').strftime('%Y-%m-%d')
			until = datetime.datetime.strptime(until, '%d/%m/%Y').strftime('%Y-%m-%d')
			cquery = "and created >= Date('{0}') and created < DATE_ADD(DATE('{1}'), INTERVAL 1 DAY) ".format(since, until)

		if branch and branch != '':
			bquery = " and branch_id = {0} ".format(branch)

		query = """select company, count(*) as posts, sum(comments) as comments, 
					sum(likes) as likes, sum(shares) as shares
					from facebook
					where company='{0}' 
					{1}
					{2}
					and getifweekend(created)='Weekend' 
					group by company 
					order by likes desc""".format(company.strip(), cquery, bquery)
		res = cdict.execute(query)
	else:
		if since and until and str(since).strip()!='' and str(until).strip()!='':
			since = datetime.datetime.strptime(since, '%d/%m/%Y').strftime('%Y-%m-%d')
			until = datetime.datetime.strptime(until, '%d/%m/%Y').strftime('%Y-%m-%d')
			cquery = "and created >= Date('{0}') and created < DATE_ADD(DATE('{1}'), INTERVAL 1 DAY) ".format(since, until)
			if branch and branch != '':
				bquery = " and branch_id = {0} ".format(branch)
		else:
			if branch and branch != '':
				bquery = " and branch_id = {0} ".format(branch)

		query = """select company, count(*) as posts, sum(comments) as comments, 
					sum(likes) as likes, sum(shares) as shares
					from facebook
					where getifweekend(created)='Weekend'
					{0}
					{1}
					group by company 
					order by likes desc""".format(cquery, bquery)
		res = cdict.execute(query)

	data = cdict.fetchall()
	conn.commit()
	cdict.close()
	conn.close()
	gc.collect()

	return data


def get_twitter_sums_per_weekend(company, since, until, branch):

	c, conn, cdict = connection()

	conn.set_character_set('utf8')
	cdict.execute('SET NAMES utf8;')
	cdict.execute('SET CHARACTER SET utf8;')
	cdict.execute('SET character_set_connection=utf8;')
	cdict.execute("set session sql_mode='';")
	conn.commit()

	cquery=''
	bquery=''

	if company and company != '':
		if since and until and str(since).strip()!='' and str(until).strip()!='':
			since = datetime.datetime.strptime(since, '%d/%m/%Y').strftime('%Y-%m-%d')
			until = datetime.datetime.strptime(until, '%d/%m/%Y').strftime('%Y-%m-%d')
			cquery = "and created >= Date('{0}') and created < DATE_ADD(DATE('{1}'), INTERVAL 1 DAY) ".format(since, until)

		if branch and branch != '':
			bquery = " and branch_id = {0} ".format(branch)

		query = """select company, count(*) as tweets, 
					sum(favorites) as favorites, sum(retweets) as retweets
					from twitter
					where company='{0}' 
					{1}
					{2}
					and getifweekend(created)='Weekend' 
					group by company 
					order by favorites desc""".format(company.strip(), cquery, bquery)
		res = cdict.execute(query)
	else:
		if since and until and str(since).strip()!='' and str(until).strip()!='':
			since = datetime.datetime.strptime(since, '%d/%m/%Y').strftime('%Y-%m-%d')
			until = datetime.datetime.strptime(until, '%d/%m/%Y').strftime('%Y-%m-%d')
			cquery = "and created >= Date('{0}') and created < DATE_ADD(DATE('{1}'), INTERVAL 1 DAY) ".format(since, until)

			if branch and branch != '':
				bquery = " and branch_id = {0} ".format(branch)
		else:
			if branch and branch != '':
				bquery = " and branch_id = {0} ".format(branch)

		query = """select company, count(*) as tweets, 
					sum(favorites) as favorites, sum(retweets) as retweets
					from twitter
					where getifweekend(created)='Weekend'
					{0}
					{1}
					group by company 
					order by favorites desc""".format(cquery, bquery)
		res = cdict.execute(query)

	data = cdict.fetchall()
	conn.commit()
	cdict.close()
	conn.close()
	gc.collect()

	return data




def get_fb_sums_per_branch(since, until, branch, bc):

	if bc and bc != '':
		if not branch or branch == '':
			return null

	c, conn, cdict = connection()

	conn.set_character_set('utf8')
	cdict.execute('SET NAMES utf8;')
	cdict.execute('SET CHARACTER SET utf8;')
	cdict.execute('SET character_set_connection=utf8;')
	cdict.execute("set session sql_mode='';")
	conn.commit()

	cquery=''
	bquery=''
	groupquery = 'group by branches.id'

	if bc and bc != '':
		groupquery = 'group by company'


	if since and until and str(since).strip()!='' and str(until).strip()!='':
		since = datetime.datetime.strptime(since, '%d/%m/%Y').strftime('%Y-%m-%d')
		until = datetime.datetime.strptime(until, '%d/%m/%Y').strftime('%Y-%m-%d')
		cquery = "and created >= Date('{0}') and created < DATE_ADD(DATE('{1}'), INTERVAL 1 DAY) ".format(since, until)
		if branch and branch != '':
			bquery = " and branch_id = {0} ".format(branch)
	else:
		if branch and branch != '':
			bquery = " and branch_id = {0} ".format(branch)

	query = """select company, company_name, branches.id, branches.name as branch, count(company) as posts, 
				sum(likes) as likes, sum(shares) as shares, sum(comments) as comments
				from facebook, branches
				where facebook.branch_id = branches.id
				{0}
				{1}
				{2} 
				order by likes desc""".format(cquery, bquery, groupquery)
	res = cdict.execute(query)

	data = cdict.fetchall()
	conn.commit()
	cdict.close()
	conn.close()
	gc.collect()

	return data


def get_twitter_sums_per_branch(since, until, branch, bc):

	if bc and bc != '':
		if not branch or branch == '':
			return null

	c, conn, cdict = connection()

	conn.set_character_set('utf8')
	cdict.execute('SET NAMES utf8;')
	cdict.execute('SET CHARACTER SET utf8;')
	cdict.execute('SET character_set_connection=utf8;')
	cdict.execute("set session sql_mode='';")
	conn.commit()

	cquery=''
	bquery=''
	groupquery = 'group by branches.id'

	if bc and bc != '':
		groupquery = 'group by company'

	if since and until and str(since).strip()!='' and str(until).strip()!='':
		since = datetime.datetime.strptime(since, '%d/%m/%Y').strftime('%Y-%m-%d')
		until = datetime.datetime.strptime(until, '%d/%m/%Y').strftime('%Y-%m-%d')
		cquery = "and created >= Date('{0}') and created < DATE_ADD(DATE('{1}'), INTERVAL 1 DAY) ".format(since, until)
		if branch and branch != '':
			bquery = " and branch_id = {0} ".format(branch)
	else:
		if branch and branch != '':
			bquery = " and branch_id = {0} ".format(branch)

	query = """select company, branches.id, branches.name as branch, count(company) as tweets, 
				sum(favorites) as favorites, sum(retweets) as retweets
				from twitter, branches
				where twitter.branch_id = branches.id
				{0}
				{1}
				{2} 
				order by favorites desc""".format(cquery, bquery, groupquery)
	res = cdict.execute(query)

	data = cdict.fetchall()
	conn.commit()
	cdict.close()
	conn.close()
	gc.collect()

	return data





# ***************************************** #
# Get sums grouped by time range:
# stored function gettimerange used here:
# 
# select gettimerange(created) as timerange, 
# count(id) as posts, sum(likes) as likes,
# sum(shares) as shares, sum(comments) as comments
# from facebook
# -- where  1
# group by timerange
# order by FIELD(timerange, '12pm-6am', '6am-12am', '12am-6pm', '6pm-12pm')
# ***************************************** #

def get_fb_sums_per_timerange(company, since, until, branch):

	c, conn, cdict = connection()

	conn.set_character_set('utf8')
	cdict.execute('SET NAMES utf8;')
	cdict.execute('SET CHARACTER SET utf8;')
	cdict.execute('SET character_set_connection=utf8;')
	cdict.execute("set session sql_mode='';")
	conn.commit()

	cquery=''
	bquery=''

	if company and company != '':
		if since and until and str(since).strip()!='' and str(until).strip()!='':
			since = datetime.datetime.strptime(since, '%d/%m/%Y').strftime('%Y-%m-%d')
			until = datetime.datetime.strptime(until, '%d/%m/%Y').strftime('%Y-%m-%d')
			cquery = "and created >= Date('{0}') and created < DATE_ADD(DATE('{1}'), INTERVAL 1 DAY) ".format(since, until)

		if branch and branch != '':
			bquery = " and branch_id = {0} ".format(branch)

		query = """select gettimerange(created) as timerange, 
					count(id) as posts, sum(likes) as likes,
					sum(shares) as shares, sum(comments) as comments
					from facebook
					where company='{0}' 
					{1}
					{2}
					group by timerange
					order by FIELD(timerange, 'Night (12pm-6am)', 'Morning (6am-12am)', 'Afternoon (12am-6pm)', 'Evening (6pm-12pm)')""".format(company.strip(), cquery, bquery)
		res = cdict.execute(query)
	else:
		if since and until and str(since).strip()!='' and str(until).strip()!='':
			since = datetime.datetime.strptime(since, '%d/%m/%Y').strftime('%Y-%m-%d')
			until = datetime.datetime.strptime(until, '%d/%m/%Y').strftime('%Y-%m-%d')
			cquery = "and created >= Date('{0}') and created < DATE_ADD(DATE('{1}'), INTERVAL 1 DAY) ".format(since, until)
			if branch and branch != '':
				bquery = " and branch_id = {0} ".format(branch)
		else:
			if branch and branch != '':
				bquery = " and branch_id = {0} ".format(branch)

		query = """select gettimerange(created) as timerange, 
					count(id) as posts, sum(likes) as likes,
					sum(shares) as shares, sum(comments) as comments
					from facebook
					where 1
					{0}
					{1}
					group by timerange
					order by FIELD(timerange, 'Night (12pm-6am)', 'Morning (6am-12am)', 'Afternoon (12am-6pm)', 'Evening (6pm-12pm)')""".format(cquery, bquery)
		res = cdict.execute(query)

	data = cdict.fetchall()
	conn.commit()
	cdict.close()
	conn.close()
	gc.collect()

	return data






# select gettimerange(created) as timerange, 
# count(id) as tweets, sum(favorites) as favorites,
# sum(retweets) as retweets
# from twitter
# -- where  1
# group by timerange
# order by FIELD(timerange, 'Night (12pm-6am)', 'Morning (6am-12am)', 'Afternoon (12am-6pm)', 'Evening (6pm-12pm)')

def get_twitter_sums_per_timerange(company, since, until, branch):

	c, conn, cdict = connection()

	conn.set_character_set('utf8')
	cdict.execute('SET NAMES utf8;')
	cdict.execute('SET CHARACTER SET utf8;')
	cdict.execute('SET character_set_connection=utf8;')
	cdict.execute("set session sql_mode='';")
	conn.commit()

	cquery=''
	bquery=''

	if company and company != '':
		if since and until and str(since).strip()!='' and str(until).strip()!='':
			since = datetime.datetime.strptime(since, '%d/%m/%Y').strftime('%Y-%m-%d')
			until = datetime.datetime.strptime(until, '%d/%m/%Y').strftime('%Y-%m-%d')
			cquery = "and created >= Date('{0}') and created < DATE_ADD(DATE('{1}'), INTERVAL 1 DAY) ".format(since, until)

		if branch and branch != '':
			bquery = " and branch_id = {0} ".format(branch)

		query = """select gettimerange(created) as timerange, 
					count(id) as tweets, sum(favorites) as favorites,
					sum(retweets) as retweets
					from twitter
					where company='{0}' 
					{1}
					{2}
					group by timerange
					order by FIELD(timerange, 'Night (12pm-6am)', 'Morning (6am-12am)', 'Afternoon (12am-6pm)', 'Evening (6pm-12pm)')""".format(company.strip(), cquery, bquery)
		res = cdict.execute(query)
	else:
		if since and until and str(since).strip()!='' and str(until).strip()!='':
			since = datetime.datetime.strptime(since, '%d/%m/%Y').strftime('%Y-%m-%d')
			until = datetime.datetime.strptime(until, '%d/%m/%Y').strftime('%Y-%m-%d')
			cquery = "and created >= Date('{0}') and created < DATE_ADD(DATE('{1}'), INTERVAL 1 DAY) ".format(since, until)
			if branch and branch != '':
				bquery = " and branch_id = {0} ".format(branch)
		else:
			if branch and branch != '':
				bquery = " and branch_id = {0} ".format(branch)

		query = """select gettimerange(created) as timerange, 
					count(id) as tweets, sum(favorites) as favorites,
					sum(retweets) as retweets
					from twitter
					where 1
					{0}
					{1}
					group by timerange
					order by FIELD(timerange, 'Night (12pm-6am)', 'Morning (6am-12am)', 'Afternoon (12am-6pm)', 'Evening (6pm-12pm)')""".format(cquery, bquery)
		res = cdict.execute(query)

	data = cdict.fetchall()
	conn.commit()
	cdict.close()
	conn.close()
	gc.collect()

	return data




# select getifweekend(created) as weekday, company, 
# company_name, count(*) as posts, 
# sum(likes) as likes, sum(shares) as shares, 
# sum(comments) as comments
# from facebook
# where 1
# group by weekday, company
# order by company, weekday

def get_fb_sums_per_weekdays_weekends(company, since, until, branch):

	c, conn, cdict = connection()

	conn.set_character_set('utf8')
	cdict.execute('SET NAMES utf8;')
	cdict.execute('SET CHARACTER SET utf8;')
	cdict.execute('SET character_set_connection=utf8;')
	cdict.execute("set session sql_mode='';")
	conn.commit()

	cquery=''
	bquery = ''

	if since and until and str(since).strip()!='' and str(until).strip()!='':

		if company and company != '':
			cquery = "and company = '{0}' ".format(company)
		
		if branch and branch != '':
			bquery = " and branch_id = {0} ".format(branch)

		since = datetime.datetime.strptime(since, '%d/%m/%Y').strftime('%Y-%m-%d')
		until = datetime.datetime.strptime(until, '%d/%m/%Y').strftime('%Y-%m-%d')
		query = """select getifweekend(created) as weekday, company, 
					company_name, count(*) as posts, 
					sum(likes) as likes, sum(shares) as shares, 
					sum(comments) as comments
					from facebook
					where created >= Date("{0}")
					and created < DATE_ADD(DATE('{1}'), INTERVAL 1 DAY)
					{2}
					{3}
					group by weekday, company 
					order by company,  
					FIELD(weekday, 'Weekday', 'Weekend')""".format(since, until, cquery, bquery)
		res = cdict.execute(query)
	else:

		if company and company != '':
			cquery = "where company = '{0}' ".format(company)
			if branch and branch != '':
				bquery = " and branch_id = {0} ".format(branch)
		else:
			if branch and branch != '':
				bquery = " where branch_id = {0} ".format(branch)

		query = """select getifweekend(created) as weekday, company, 
					company_name, count(*) as posts, 
					sum(likes) as likes, sum(shares) as shares, 
					sum(comments) as comments
					from facebook
					{0}
					{1}
					group by weekday, company 
					order by company,  
					FIELD(weekday, 'Weekday', 'Weekend')""".format(cquery, bquery)
		res = cdict.execute(query)

	data = cdict.fetchall()
	conn.commit()
	cdict.close()
	conn.close()
	gc.collect()

	return data





def get_twitter_sums_per_weekdays_weekends(company, since, until, branch):

	c, conn, cdict = connection()

	conn.set_character_set('utf8')
	cdict.execute('SET NAMES utf8;')
	cdict.execute('SET CHARACTER SET utf8;')
	cdict.execute('SET character_set_connection=utf8;')
	cdict.execute("set session sql_mode='';")
	conn.commit()

	cquery=''
	bquery = ''

	if since and until and str(since).strip()!='' and str(until).strip()!='':

		if company and company != '':
			cquery = "and company = '{0}' ".format(company)
		
		if branch and branch != '':
			bquery = " and branch_id = {0} ".format(branch)

		since = datetime.datetime.strptime(since, '%d/%m/%Y').strftime('%Y-%m-%d')
		until = datetime.datetime.strptime(until, '%d/%m/%Y').strftime('%Y-%m-%d')
		query = """select getifweekend(created) as weekday, company, 
					count(*) as tweets, 
					sum(favorites) as favorites, sum(retweets) as retweets
					from twitter
					where created >= Date("{0}")
					and created < DATE_ADD(DATE('{1}'), INTERVAL 1 DAY)
					{2}
					{3}
					group by weekday, company 
					order by company,  
					FIELD(weekday, 'Weekday', 'Weekend')""".format(since, until, cquery, bquery)
		res = cdict.execute(query)
	else:

		if company and company != '':
			cquery = "where company = '{0}' ".format(company)
			if branch and branch != '':
				bquery = " and branch_id = {0} ".format(branch)
		else:
			if branch and branch != '':
				bquery = " where branch_id = {0} ".format(branch)

		query = """select getifweekend(created) as weekday, company, 
					count(*) as tweets, 
					sum(favorites) as favorites, sum(retweets) as retweets
					from twitter
					{0}
					{1}
					group by weekday, company 
					order by company,  
					FIELD(weekday, 'Weekday', 'Weekend')""".format(cquery, bquery)
		res = cdict.execute(query)
		
	data = cdict.fetchall()
	conn.commit()
	cdict.close()
	conn.close()
	gc.collect()

	return data





def get_fb_sums_per_char_range(company, since, until, branch):

	c, conn, cdict = connection()

	conn.set_character_set('utf8')
	cdict.execute('SET NAMES utf8;')
	cdict.execute('SET CHARACTER SET utf8;')
	cdict.execute('SET character_set_connection=utf8;')
	cdict.execute("set session sql_mode='';")
	conn.commit()

	cquery=''
	bquery = ''

	if since and until and str(since).strip()!='' and str(until).strip()!='':

		if company and company != '':
			cquery = "and company = '{0}' ".format(company)
		
		if branch and branch != '':
			bquery = " and branch_id = {0} ".format(branch)

		since = datetime.datetime.strptime(since, '%d/%m/%Y').strftime('%Y-%m-%d')
		until = datetime.datetime.strptime(until, '%d/%m/%Y').strftime('%Y-%m-%d')
		query = """select company, company_name,
					count(*) as posts, getcharrange(message) as charrange,  
					sum(likes) as likes, sum(shares) as shares, 
					sum(comments) as comments
					from facebook
					where created >= Date("{0}")
					and created < DATE_ADD(DATE('{1}'), INTERVAL 1 DAY)
					{2}
					{3}
					group by charrange, company
					order by 
					company, 
					FIELD(charrange, '<=100', '101-200', '201-300', '301-400', '401-500', '>500'),
					posts""".format(since, until, cquery, bquery)
		res = cdict.execute(query)
	else:

		if company and company != '':
			cquery = "where company = '{0}' ".format(company)
			if branch and branch != '':
				bquery = " and branch_id = {0} ".format(branch)
		else:
			if branch and branch != '':
				bquery = " where branch_id = {0} ".format(branch)

		query = """select company, company_name,
					count(*) as posts, getcharrange(message) as charrange,  
					sum(likes) as likes, sum(shares) as shares, 
					sum(comments) as comments
					from facebook
					{0}
					{1}
					group by charrange, company
					order by 
					company, 
					FIELD(charrange, '<=100', '101-200', '201-300', '301-400', '401-500', '>500'),
					posts""".format(cquery, bquery)
		res = cdict.execute(query)

	data = cdict.fetchall()
	conn.commit()
	cdict.close()
	conn.close()
	gc.collect()

	return data




def get_twitter_sums_per_char_range(company, since, until, branch):

	c, conn, cdict = connection()

	conn.set_character_set('utf8')
	cdict.execute('SET NAMES utf8;')
	cdict.execute('SET CHARACTER SET utf8;')
	cdict.execute('SET character_set_connection=utf8;')
	cdict.execute("set session sql_mode='';")
	conn.commit()

	cquery=''
	bquery = ''

	if since and until and str(since).strip()!='' and str(until).strip()!='':

		if company and company != '':
			cquery = "and company = '{0}' ".format(company)
		
		if branch and branch != '':
			bquery = " and branch_id = {0} ".format(branch)

		since = datetime.datetime.strptime(since, '%d/%m/%Y').strftime('%Y-%m-%d')
		until = datetime.datetime.strptime(until, '%d/%m/%Y').strftime('%Y-%m-%d')
		query = """select company,
					count(*) as tweets, getcharrange(text) as charrange,  
					sum(favorites) as favorites, sum(retweets) as retweets
					from twitter
					where created >= Date("{0}")
					and created < DATE_ADD(DATE('{1}'), INTERVAL 1 DAY)
					{2}
					{3}
					group by charrange, company
					order by 
					company, 
					FIELD(charrange, '<=100', '101-200', '201-300', '301-400', '401-500', '>500'),
					tweets""".format(since, until, cquery, bquery)
		res = cdict.execute(query)
	else:

		if company and company != '':
			cquery = "where company = '{0}' ".format(company)
			if branch and branch != '':
				bquery = " and branch_id = {0} ".format(branch)
		else:
			if branch and branch != '':
				bquery = " where branch_id = {0} ".format(branch)

		query = """select company,
					count(*) as tweets, getcharrange(text) as charrange,  
					sum(favorites) as favorites, sum(retweets) as retweets
					from twitter
					{0}
					{1}
					group by charrange, company
					order by 
					company, 
					FIELD(charrange, '<=100', '101-200', '201-300', '301-400', '401-500', '>500'),
					tweets""".format(cquery, bquery)
		res = cdict.execute(query)

	data = cdict.fetchall()
	conn.commit()
	cdict.close()
	conn.close()
	gc.collect()

	return data



def get_fb_sums_per_day(company, since, until, branch):

	c, conn, cdict = connection()

	conn.set_character_set('utf8')
	cdict.execute('SET NAMES utf8;')
	cdict.execute('SET CHARACTER SET utf8;')
	cdict.execute('SET character_set_connection=utf8;')
	cdict.execute("set session sql_mode='';")
	conn.commit()

	cquery=''
	bquery = ''

	if since and until and str(since).strip()!='' and str(until).strip()!='':

		if company and company != '':
			cquery = "and company = '{0}' ".format(company)
		
		if branch and branch != '':
			bquery = " and branch_id = {0} ".format(branch)

		since = datetime.datetime.strptime(since, '%d/%m/%Y').strftime('%Y-%m-%d')
		until = datetime.datetime.strptime(until, '%d/%m/%Y').strftime('%Y-%m-%d')
		query = """select company, count(*) as posts, 
					sum(likes) as likes, sum(shares) as shares, 
					sum(comments) as comments, DATE(created) as day 
					from facebook 
					where created >= Date("{0}")
					and created < DATE_ADD(DATE('{1}'), INTERVAL 1 DAY)
					{2}
					{3}
					group by company, day order by company, day""".format(since, until, cquery, bquery)
		res = cdict.execute(query)
	else:

		if company and company != '':
			cquery = "where company = '{0}' ".format(company)
			if branch and branch != '':
				bquery = " and branch_id = {0} ".format(branch)
		else:
			if branch and branch != '':
				bquery = " where branch_id = {0} ".format(branch)

		query = """select company, count(*) as posts, 
					sum(likes) as likes, sum(shares) as shares, 
					sum(comments) as comments, DATE(created) as day 
					from facebook
					{0}
					{1}
					group by company, day order by company, day""".format(cquery, bquery)
		res = cdict.execute(query)
	data = cdict.fetchall()
	conn.commit()
	cdict.close()
	conn.close()
	gc.collect()

	return data





def get_twitter_sums_per_day(company, since, until, branch):

	c, conn, cdict = connection()

	conn.set_character_set('utf8')
	cdict.execute('SET NAMES utf8;')
	cdict.execute('SET CHARACTER SET utf8;')
	cdict.execute('SET character_set_connection=utf8;')
	cdict.execute("set session sql_mode='';")
	conn.commit()

	cquery=''
	bquery = ''

	if since and until and str(since).strip()!='' and str(until).strip()!='':

		if company and company != '':
			cquery = "and company = '{0}'".format(company)
		
		if branch and branch != '':
			bquery = " and branch_id = {0} ".format(branch)

		since = datetime.datetime.strptime(since, '%d/%m/%Y').strftime('%Y-%m-%d')
		until = datetime.datetime.strptime(until, '%d/%m/%Y').strftime('%Y-%m-%d')
		query = """select company, count(*) as tweets, 
					sum(favorites) as favorites, sum(retweets) as retweets,
					DATE(created) as day 
					from twitter 
					where created >= Date("{0}")
					and created < DATE_ADD(DATE('{1}'), INTERVAL 1 DAY)
					{2}
					{3}
					group by company, day order by company, day""".format(since, until, cquery, bquery)
		res = cdict.execute(query)
	else:

		if company and company != '':
			cquery = "where company = '{0}'".format(company)
			if branch and branch != '':
				bquery = " and branch_id = {0} ".format(branch)
		else:
			if branch and branch != '':
				bquery = " where branch_id = {0} ".format(branch)

		query = """select company, count(*) as tweets, 
					sum(favorites) as favorites, sum(retweets) as retweets,
					DATE(created) as day 
					from twitter
					{0}
					{1}
					group by company, day order by company, day""".format(cquery, bquery)
		res = cdict.execute(query)
	data = cdict.fetchall()
	conn.commit()
	cdict.close()
	conn.close()
	gc.collect()

	return data
