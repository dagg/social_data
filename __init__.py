# -*- coding: utf-8 -*-

from flask import Flask, render_template, flash, request, url_for, redirect, session
from content_management import Content
# from twitterparser import TwitterParser
from twitterparser_daterange import TwitterParser, delete_existingT
# from fbparser import FBParser
from fbparser_daterange_new import FBParser, delete_existing
# from googleplusparser import GooglePlusParser
# from googleplusparser_moreresults import GooglePlusParser
from googleplusparser_daterangeresults import GooglePlusParser, delete_existingGP

from get_googleplus_chart_data import getGPData, getGPChartData

from dbconnect import connection

from wtforms import Form, BooleanField, TextField, PasswordField, validators

from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart

# from get_facebook_chart_data import getData
from get_facebook_chart_data import getData, getChartData

from get_twitter_chart_data import getTData, getTChartData

import gc
import urllib
from urllib import quote_plus

from get_db_data import get_fb_data, get_twitter_data, get_googleplus_data, get_branches

#more charts/tables queries in DAO
from DAO.dao import *

import datetime

TOPIC_DICT = Content()

app = Flask(__name__)

def wordcount(x):
	if x:
		return len(x.split(' '))
	else:
		return None

def get_weekday(date):
	if date:
		return datetime.datetime.strptime(str(date).split('.')[0], '%Y-%m-%d %H:%M:%S').strftime('%A')
	else:
		return None

app.jinja_env.filters['quote_plus'] = lambda u: urllib.quote_plus(u)
app.jinja_env.filters['wordcount'] = lambda x: wordcount(x)
app.jinja_env.filters['getweekday'] = lambda x: get_weekday(x)

# set the secret key.  keep this really secret:
app.secret_key = 'flasksecretforsocialappproject'

datetimeformat = '%Y-%m-%d %H:%M:%S'

@app.route('/')
def homepage():
	print "From Homepage. IP: "+str(request.remote_addr)
	return render_template("header.html", bg='full')

@app.route('/facebook/')
def facebook():
	flash('Flashing Test!!!')
	return render_template("facebook.html", TOPIC_DICT = TOPIC_DICT)


############ FACEBOOK ############
@app.route('/facebookform/', methods=['GET', 'POST'])
def facebookform():
	print "From Facebook. IP: "+str(request.remote_addr)

	branches = get_branches()

	if request.method == "POST":
		company = request.form['company']
		# population = request.form['population']
		since = request.form['since']
		until = request.form['until']

		branch = request.form['branch']

		delete = 1
		if request.form.get('nodelete') and request.form.get('nodelete')=='on':
			delete = 0
		# if not population:
		# 	population=200
		if not since or not until or str(since).strip()=='' or str(until).strip()=='':
			flash("Please give the Since/Until dates ")
			return render_template("facebookform.html", branches=branches)

		if company:
			print "From Facebook. IP: "+str(request.remote_addr)+" Company: "+company.strip()+", Since:"+ since +" Until:"+ until
			# fbs=FBParser([company.strip()], population)
			fbs, followers, company_name=FBParser([company.strip()], since, until, delete, branch)
			return render_template("facebook.html", fbs=fbs, followers=followers, company_name=company_name, title="Facebook Data Retrieval")
		else:
			flash("Please give a company name")
		# pass

	return render_template("facebookform.html", branches=branches)



# print get_fb_data( 'cosmote', None, None )
@app.route('/facebookdataform/', methods=['GET', 'POST'])
def facebookdataform():
	print "From Facebook data. IP: "+str(request.remote_addr)
	if request.method == "POST":

		# company = request.form['company']
		company = request.form.get('company')
		# population = request.form['population']
		since = request.form['since']
		until = request.form['until']

		print "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
		print "Company: %s, Since: %s, Until: %s" % (company, since, until)
		print "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"

		if company:
			print "From Facebook data. IP: "+str(request.remote_addr)+" Company: "+company.strip()+", Since:"+ since +" Until:"+ until
			# fbs=FBParser([company.strip()], population)
			fbs, company_name, followers, branch = get_fb_data(company.strip(), since, until)
			return render_template("facebookdata.html", fbs=fbs, company_name=company_name, followers=followers, branch=branch, title="Facebook Data Retrieval")
		else:
			flash("Please give a company name")
		# pass

	data = getData("deletecompany")
	return render_template("facebookdataform.html", fbs=data)



@app.route('/facebookcharts/', methods=['GET', 'POST'])
def facebookcharts():

	print "From Facebook Charts. IP: "+str(request.remote_addr)

	template = "social_charts/facebookchartsform.html"

	options={
    "aggregate":"social_charts/facebookcharts.html",
    "posts":"social_charts/facebookpostscharts.html",
    "shares":"social_charts/facebooksharescharts.html",
    "likes":"social_charts/facebooklikescharts.html",
    "comments":"social_charts/facebookcommentscharts.html",
    "deletecompany":"social_charts/facebookdeletecompany.html"
	}

	# f = request.form
	# for key in f.keys():
	# 	for value in f.getlist(key):
	# 		print key,":",value

	action = request.form.get('param')
	since = request.form.get('since')
	until = request.form.get('until')
	data = None

	if action and action in options:
		print "From Facebook Charts. IP: "+str(request.remote_addr)+" Action: "+action+", Since:"+ since +" Until:"+ until
		template = options[action]
		if not since or not until or str(since).strip()=='' or str(until).strip()=='':
			flash("Please give the Since/Until dates ")
			return render_template("social_charts/facebookchartsform.html", title="Facebook Data Retrieval")
		
		data = getChartData(action, since, until)

	return render_template(template, fbs=data, since=since, until=until, title="Facebook Data Retrieval")



@app.route('/facebookcharts_sums_per_weekday/', methods=['GET', 'POST'])
def facebookcharts_sums_per_weekday():

	print "From Facebook Charts. IP: "+str(request.remote_addr)

	template = "social_charts/facebookcharts_sums_per_weekday.html"

	branches = get_branches()

	branch = request.form.get('branch')

	action = request.form.get('param')
	since = request.form.get('since')
	until = request.form.get('until')
	company = request.form.get('company')

	data = None

	if action:
		if not since or not until or str(since).strip()=='' or str(until).strip()=='':
			data = get_fb_sums_per_weekdays(company, None, None, branch)
		else:
			data = get_fb_sums_per_weekdays(company, since, until, branch)
	else:
		data = getData("deletecompany")
		template="social_charts/facebookmorechartsform.html"

	return render_template(template, company=company, branches=branches, qaction=action, fbs=data, since=since, until=until, msg="Give the dates (optional/experimental):", notlist=0, chart_type="facebookcharts_sums_per_weekday", title="Companies per weekday")



@app.route('/facebookcharts_sums_per_day/', methods=['GET', 'POST'])
def facebookcharts_sums_per_day():

	print "From Facebook Charts. IP: "+str(request.remote_addr)

	template = "social_charts/facebookcharts_sums_per_day.html"

	branches = get_branches()

	branch = request.form.get('branch')

	action = request.form.get('param')
	since = request.form.get('since')
	until = request.form.get('until')
	company = request.form.get('company')

	data = None

	if action:
		if not since or not until or str(since).strip()=='' or str(until).strip()=='':
			data = get_fb_sums_per_day(company, None, None, branch)
		else:
			data = get_fb_sums_per_day(company, since, until, branch)
	else:
		data = getData("deletecompany")
		template="social_charts/facebookmorechartsform.html"

	return render_template(template, company=company, branches=branches, qaction=action, fbs=data, since=since, until=until, msg="Give the dates (optional/experimental):", notlist=0, chart_type="facebookcharts_sums_per_day", title="Companies per day")




@app.route('/facebookcharts_sums_per_month/', methods=['GET', 'POST'])
def facebookcharts_sums_per_month():

	print "From Facebook Charts. IP: "+str(request.remote_addr)

	template = "social_charts/facebookcharts_sums_per_month.html"

	branches = get_branches()

	branch = request.form.get('branch')

	action = request.form.get('param')
	since = request.form.get('since')
	until = request.form.get('until')
	company = request.form.get('company')
	data = None

	if action:
		if not since or not until or str(since).strip()=='' or str(until).strip()=='':
			data = get_fb_sums_per_month(company, None, None, branch)
		else:
			data = get_fb_sums_per_month(company, since, until, branch)
	else:
		data = getData("deletecompany")
		template="social_charts/facebookmorechartsform.html"

	return render_template(template, company=company, branches=branches, qaction=action, fbs=data, since=since, until=until, msg="Give the dates (optional/experimental):", notlist=0, chart_type="facebookcharts_sums_per_month", title="Companies per month")


@app.route('/facebookcharts_sums_per_type/', methods=['GET', 'POST'])
def facebookcharts_sums_per_type():

	print "From Facebook Charts. IP: "+str(request.remote_addr)

	template = "social_charts/facebookcharts_sums_per_type.html"

	branches = get_branches()

	branch = request.form.get('branch')

	action = request.form.get('param')
	since = request.form.get('since')
	until = request.form.get('until')
	company = request.form.get('company')
	data = None

	if action:
		if not since or not until or str(since).strip()=='' or str(until).strip()=='':
			data = get_fb_sums_per_type(company, None, None, branch)
		else:
			data = get_fb_sums_per_type(company, since, until, branch)
	else:
		data = getData("deletecompany")
		template="social_charts/facebookmorechartsform.html"

	return render_template(template, company=company, branches=branches, fbs=data, since=since, until=until, msg="Give the dates (optional/experimental):", notlist=1, chart_type="facebookcharts_sums_per_type", title="Companies and Types")




@app.route('/facebookcharts_sums_per_weekend/', methods=['GET', 'POST'])
def facebookcharts_sums_per_weekend():

	print "From Facebook Charts. IP: "+str(request.remote_addr)

	template = "social_charts/facebookcharts_sums_per_weekend.html"

	branches = get_branches()

	branch = request.form.get('branch')

	action = request.form.get('param')
	since = request.form.get('since')
	until = request.form.get('until')
	company = request.form.get('company')
	data = None

	if action:
		if not since or not until or str(since).strip()=='' or str(until).strip()=='':
			data = get_fb_sums_per_weekend(company, None, None, branch)
		else:
			data = get_fb_sums_per_weekend(company, since, until, branch)
	else:
		data = getData("deletecompany")
		template="social_charts/facebookmorechartsform.html"

	return render_template(template, company=company, branches=branches, qaction=action, fbs=data, since=since, until=until, msg="Give the dates (optional/experimental):", notlist=0, chart_type="facebookcharts_sums_per_weekend", title="Companies sums per Weekend")





# get_fb_sums_per_branch(since, until, branch)
@app.route('/facebookcharts_sums_per_branch/', methods=['GET', 'POST'])
def facebookcharts_sums_per_branch():

	print "From Facebook Charts. IP: "+str(request.remote_addr)

	template = "social_charts/facebookcharts_sums_per_branch.html"

	branches = get_branches()

	branch = request.form.get('branch')

	action = request.form.get('param')
	since = request.form.get('since')
	until = request.form.get('until')
	# company = request.form.get('company')
	data = None

	if action:
		if not since or not until or str(since).strip()=='' or str(until).strip()=='':
			data = get_fb_sums_per_branch(None, None, branch, None)
		else:
			data = get_fb_sums_per_branch(since, until, branch, None)
	else:
		data = getData("deletecompany")
		template="social_charts/facebookmorechartsform.html"

	return render_template(template, branches=branches, nocompany=1, qaction=action, fbs=data, since=since, until=until, msg="Give the dates (optional/experimental):", notlist=0, chart_type="facebookcharts_sums_per_branch", title="Companies sums per Branch")





# get_fb_sums_per_branch(since, until, branch)
@app.route('/facebookcharts_sums_companies_per_branch/', methods=['GET', 'POST'])
def facebookcharts_sums_companies_per_branch():

	print "From Facebook Charts. IP: "+str(request.remote_addr)

	template = "social_charts/facebookcharts_sums_companies_per_branch.html"

	branches = get_branches()

	branch = request.form.get('branch')

	action = request.form.get('param')
	since = request.form.get('since')
	until = request.form.get('until')
	# company = request.form.get('company')
	data = None

	if action:
		if not branch:
			flash("Please give a Branch")
			data = getData("deletecompany")
			template="social_charts/facebookmorechartsform.html"
			return render_template(template, branches=branches, nocompany=1, qaction=action, fbs=data, since=since, until=until, msg="Give the dates (optional/experimental):", notlist=0, chart_type="facebookcharts_sums_per_branch", title="Companies sums per Branch")


		if not since or not until or str(since).strip()=='' or str(until).strip()=='':
			data = get_fb_sums_per_branch(None, None, branch, 1)
		else:
			data = get_fb_sums_per_branch(since, until, branch, 1)
	else:
		data = getData("deletecompany")
		template="social_charts/facebookmorechartsform.html"

	return render_template(template, branches=branches, nocompany=1, qaction=action, fbs=data, since=since, until=until, msg="Give the dates (optional/experimental):", notlist=0, chart_type="facebookcharts_sums_per_branch", title="Companies sums per Branch")








@app.route('/facebookcharts_sums_per_timerange/', methods=['GET', 'POST'])
def facebookcharts_sums_per_timerange():

	print "From Facebook Charts. IP: "+str(request.remote_addr)

	template = "social_charts/facebookcharts_sums_per_timerange.html"

	branches = get_branches()

	branch = request.form.get('branch')

	action = request.form.get('param')
	since = request.form.get('since')
	until = request.form.get('until')
	company = request.form.get('company')
	data = None

	if action:
		if not since or not until or str(since).strip()=='' or str(until).strip()=='':
			data = get_fb_sums_per_timerange(company, None, None, branch)
		else:
			data = get_fb_sums_per_timerange(company, since, until, branch)
	else:
		data = getData("deletecompany")
		template="social_charts/facebookmorechartsform.html"

	return render_template(template, company=company, branches=branches, qaction=action, fbs=data, since=since, until=until, msg="Give the dates (optional/experimental):", notlist=0, chart_type="facebookcharts_sums_per_timerange", title="Companies sums per Time Range")





@app.route('/facebookcharts_sums_per_weekday_weekend/', methods=['GET', 'POST'])
def facebookcharts_sums_per_weekday_weekend():

	print "From Facebook Charts. IP: "+str(request.remote_addr)

	template = "social_charts/facebookcharts_sums_per_weekday_weekend.html"

	branches = get_branches()

	branch = request.form.get('branch')

	action = request.form.get('param')
	since = request.form.get('since')
	until = request.form.get('until')
	company = request.form.get('company')

	data = None

	if action:
		if not since or not until or str(since).strip()=='' or str(until).strip()=='':
			data = get_fb_sums_per_weekdays_weekends(company, None, None, branch)
		else:
			data = get_fb_sums_per_weekdays_weekends(company, since, until, branch)
	else:
		data = getData("deletecompany")
		template="social_charts/facebookmorechartsform.html"

	return render_template(template, company=company, branches=branches, qaction=action, fbs=data, since=since, until=until, msg="Give the dates (optional/experimental):", notlist=0, chart_type="facebookcharts_sums_per_weekday_weekend", title="Companies per weekday/weekend")




@app.route('/facebookcharts_sums_per_char_range/', methods=['GET', 'POST'])
def facebookcharts_sums_per_char_range():

	print "From Facebook Charts. IP: "+str(request.remote_addr)

	template = "social_charts/facebookcharts_sums_per_char_range.html"

	branches = get_branches()

	branch = request.form.get('branch')

	action = request.form.get('param')
	since = request.form.get('since')
	until = request.form.get('until')
	company = request.form.get('company')

	data = None

	if action:
		if not since or not until or str(since).strip()=='' or str(until).strip()=='':
			data = get_fb_sums_per_char_range(company, None, None, branch)
		else:
			data = get_fb_sums_per_char_range(company, since, until, branch)
	else:
		data = getData("deletecompany")
		template="social_charts/facebookmorechartsform.html"

	return render_template(template, company=company, branches=branches, qaction=action, fbs=data, since=since, until=until, msg="Give the dates (optional/experimental):", notlist=0, chart_type="facebookcharts_sums_per_chars_range", title="Companies per character range")





@app.route('/deletefbcompany/', methods=['GET', 'POST'])
def deletecompany():
	company = request.args.get('company')
	
	if company:
		print "From Facebook Delete Company. IP: "+str(request.remote_addr)+" Company: "+company
		result = delete_existing(company)
		if int(result) >= 0:
			flash("Company %s deleted successfully!" % company)

	data = getData("deletecompany")
	return render_template("social_charts/facebookdeletecompany.html", fbs=data, title="Delete Facebook Company")


	

############ TWITTER ############
@app.route('/twitterform/', methods=['GET', 'POST'])
def twitterform():
	print "From Twitter. IP: "+str(request.remote_addr)

	branches = get_branches()

	if request.method == "POST":
		company = request.form['company']

		since = request.form['since']
		until = request.form['until']

		branch = request.form['branch']

		delete = 1
		if request.form.get('nodelete') and request.form.get('nodelete')=='on':
			delete = 0

		# if not population:
		# 	population=200
		if not since or not until or str(since).strip()=='' or str(until).strip()=='':
			flash("Please give the Since/Until dates ")
			return render_template("twitterform.html", branches=branches)

		if company:
			print "From Twitter. IP: "+str(request.remote_addr)+" Company: "+company.strip()+", Since:"+ since +" Until:"+ until
			tweets=TwitterParser(company.strip(), since, until, delete, branch)
			return render_template("twitter.html", tweets=tweets, title="Tweeter Data Retrieval")
		else:
			flash("Please give a company name")
		# pass

	return render_template("twitterform.html", branches=branches)




@app.route('/deletetwittercompany/', methods=['GET', 'POST'])
def deleteTcompany():
	company = request.args.get('company')

	if company:
		print "From Twitter Delete Company. IP: "+str(request.remote_addr)+" Company: "+company
		result = delete_existingT(company)
		if int(result) >= 0:
			flash("Company %s deleted successfully!" % company)

	data = getTData("deletecompany")
	return render_template("social_charts/twitterdeletecompany.html", fbs=data, title="Delete Twitter Company")


@app.route('/twitterdataform/', methods=['GET', 'POST'])
def twitterdataform():
	print "From Twitter data. IP: "+str(request.remote_addr)
	if request.method == "POST":

		company = request.form.get('company')
		since = request.form['since']
		until = request.form['until']

		if company:
			print "From Twitter data. IP: "+str(request.remote_addr)+" Company: "+company.strip()+", Since:"+ since +" Until:"+ until
			# fbs=FBParser([company.strip()], population)
			data, company_name, branch = get_twitter_data(company.strip(), since, until)
			return render_template("twitterdata.html", tweets=data, company=company, branch=branch, title="Twitter Data Retrieval")
		else:
			flash("Please give a company name")
		# pass

	data = getTData("deletecompany")
	return render_template("twitterdataform.html", fbs=data)



@app.route('/twittercharts/', methods=['GET', 'POST'])
def twittercharts():

	print "From Twitter Charts. IP: "+str(request.remote_addr)

	template = "social_charts/twitterchartsform.html"

	options={
    "aggregate":"social_charts/twittercharts.html",
    "posts":"social_charts/twitterpostscharts.html",
    "favorites":"social_charts/twitterfavoritescharts.html",
    "retweets":"social_charts/twitterretweetscharts.html",
    "deletecompany":"social_charts/twitterdeletecompany.html"
	}

	# f = request.form
	# for key in f.keys():
	# 	for value in f.getlist(key):
	# 		print key,":",value

	action = request.form.get('param')
	since = request.form.get('since')
	until = request.form.get('until')
	data = None

	if action and action in options:
		print "From Twitter Charts. IP: "+str(request.remote_addr)+" Action: "+action+", Since:"+ since +" Until:"+ until
		template = options[action]
		if not since or not until or str(since).strip()=='' or str(until).strip()=='':
			flash("Please give the Since/Until dates ")
			return render_template("social_charts/twitterchartsform.html", title="Twitter Data Retrieval")
		
		data = getTChartData(action, since, until)

	return render_template(template, twitters=data, since=since, until=until, title="Twitter Data Retrieval")



@app.route('/twittercharts_sums_per_weekday/', methods=['GET', 'POST'])
def twittercharts_sums_per_weekday():

	branches = get_branches()

	branch = request.form.get('branch')

	print "From Twitter Charts. IP: "+str(request.remote_addr)

	template = "social_charts/twittercharts_sums_per_weekday.html"

	action = request.form.get('param')
	since = request.form.get('since')
	until = request.form.get('until')
	company = request.form.get('company')
	data = None

	if action:
		if not since or not until or str(since).strip()=='' or str(until).strip()=='':
			data = get_twitter_sums_per_weekdays(company, None, None, branch)
		else:
			data = get_twitter_sums_per_weekdays(company, since, until, branch)
	else:
		data = getTData("deletecompany")
		template="social_charts/twittermorechartsform.html"

	# return render_template(template, tweets=data, title="Twitter Data Retrieval")
	return render_template(template, company=company, branches=branches, qaction=action, tweets=data, since=since, until=until, msg="Give the dates (optional/experimental):", notlist=0, chart_type="twittercharts_sums_per_weekday", title="Companies per weekday")



@app.route('/twittercharts_sums_per_day/', methods=['GET', 'POST'])
def twittercharts_sums_per_day():

	branches = get_branches()

	branch = request.form.get('branch')

	print "From Twitter Charts. IP: "+str(request.remote_addr)

	template = "social_charts/twittercharts_sums_per_day.html"

	action = request.form.get('param')
	since = request.form.get('since')
	until = request.form.get('until')
	company = request.form.get('company')
	data = None

	if action:
		if not since or not until or str(since).strip()=='' or str(until).strip()=='':
			data = get_twitter_sums_per_day(company, None, None, branch)
		else:
			data = get_twitter_sums_per_day(company, since, until, branch)
	else:
		data = getTData("deletecompany")
		template="social_charts/twittermorechartsform.html"

	# return render_template(template, tweets=data, title="Twitter Data Retrieval")
	return render_template(template, company=company, branches=branches, qaction=action, tweets=data, since=since, until=until, msg="Give the dates (optional/experimental):", notlist=0, chart_type="twittercharts_sums_per_day", title="Companies per day")




@app.route('/twittercharts_sums_per_month/', methods=['GET', 'POST'])
def twittercharts_sums_per_month():

	print "From Facebook Charts. IP: "+str(request.remote_addr)

	template = "social_charts/twittercharts_sums_per_month.html"

	branches = get_branches()

	branch = request.form.get('branch')

	action = request.form.get('param')
	since = request.form.get('since')
	until = request.form.get('until')
	company = request.form.get('company')
	data = None

	if action:
		if not since or not until or str(since).strip()=='' or str(until).strip()=='':
			data = get_twitter_sums_per_month(company, None, None, branch)
		else:
			data = get_twitter_sums_per_month(company, since, until, branch)
	else:
		data = getTData("deletecompany")
		template="social_charts/twittermorechartsform.html"

	return render_template(template, company=company, branches=branches, qaction=action, tweets=data, since=since, until=until, msg="Give the dates (optional/experimental):", notlist=0, chart_type="twittercharts_sums_per_month", title="Companies per month")




@app.route('/twittercharts_sums_per_type/', methods=['GET', 'POST'])
def twittercharts_sums_per_type():

	print "From Facebook Charts. IP: "+str(request.remote_addr)

	template = "social_charts/twittercharts_sums_per_type.html"

	branches = get_branches()

	branch = request.form.get('branch')

	action = request.form.get('param')
	since = request.form.get('since')
	until = request.form.get('until')
	company = request.form.get('company')
	data = None

	if action:
		if not since or not until or str(since).strip()=='' or str(until).strip()=='':
			data = get_twitter_sums_per_type(company, None, None, branch)
		else:
			data = get_twitter_sums_per_type(company, since, until, branch)
	else:
		data = getTData("deletecompany")
		template="social_charts/twittermorechartsform.html"

	return render_template(template, company=company, branches=branches, tweets=data, since=since, until=until, msg="Give the dates (optional/experimental):", notlist=1, chart_type="twittercharts_sums_per_type", title="Companies and Types")




@app.route('/twittercharts_sums_per_weekend/', methods=['GET', 'POST'])
def twittercharts_sums_per_weekend():

	print "From Facebook Charts. IP: "+str(request.remote_addr)

	template = "social_charts/twittercharts_sums_per_weekend.html"

	branches = get_branches()

	branch = request.form.get('branch')

	action = request.form.get('param')
	since = request.form.get('since')
	until = request.form.get('until')
	company = request.form.get('company')
	data = None

	if action:
		if not since or not until or str(since).strip()=='' or str(until).strip()=='':
			data = get_twitter_sums_per_weekend(company, None, None, branch)
		else:
			data = get_twitter_sums_per_weekend(company, since, until, branch)
	else:
		data = getTData("deletecompany")
		template="social_charts/twittermorechartsform.html"

	return render_template(template, branches=branches, qaction=action, tweets=data, since=since, until=until, msg="Give the dates (optional/experimental):", notlist=0, chart_type="twittercharts_sums_per_weekend", title="Companies sums per Weekend")




@app.route('/twittercharts_sums_per_branch/', methods=['GET', 'POST'])
def twittercharts_sums_per_branch():

	print "From Facebook Charts. IP: "+str(request.remote_addr)

	template = "social_charts/twittercharts_sums_per_branch.html"

	branches = get_branches()

	branch = request.form.get('branch')

	action = request.form.get('param')
	since = request.form.get('since')
	until = request.form.get('until')
	data = None

	if action:
		if not since or not until or str(since).strip()=='' or str(until).strip()=='':
			data = get_twitter_sums_per_branch(None, None, branch, None)
		else:
			data = get_twitter_sums_per_branch(since, until, branch, None)
	else:
		data = getTData("deletecompany")
		template="social_charts/twittermorechartsform.html"

	return render_template(template, branches=branches, nocompany=1, qaction=action, tweets=data, since=since, until=until, msg="Give the dates (optional/experimental):", notlist=0, chart_type="twittercharts_sums_per_branch", title="Companies sums per Branch")




@app.route('/twittercharts_sums_companies_per_branch/', methods=['GET', 'POST'])
def twittercharts_sums_companies_per_branch():

	print "From Facebook Charts. IP: "+str(request.remote_addr)

	template = "social_charts/twittercharts_sums_companies_per_branch.html"

	branches = get_branches()

	branch = request.form.get('branch')

	action = request.form.get('param')
	since = request.form.get('since')
	until = request.form.get('until')
	data = None

	if action:
		if not branch:
					flash("Please give a Branch")
					data = getData("deletecompany")
					template="social_charts/twittermorechartsform.html"
					return render_template(template, branches=branches, nocompany=1, qaction=action, tweets=data, since=since, until=until, msg="Give the dates (optional/experimental):", notlist=0, chart_type="twittercharts_sums_per_branch", title="Companies sums per Branch")

		if not since or not until or str(since).strip()=='' or str(until).strip()=='':
			data = get_twitter_sums_per_branch(None, None, branch, 1)
		else:
			data = get_twitter_sums_per_branch(since, until, branch, 1)
	else:
		data = getTData("deletecompany")
		template="social_charts/twittermorechartsform.html"

	return render_template(template, branches=branches, nocompany=1, qaction=action, tweets=data, since=since, until=until, msg="Give the dates (optional/experimental):", notlist=0, chart_type="twittercharts_sums_per_branch", title="Companies sums per Branch")



@app.route('/twittercharts_sums_per_timerange/', methods=['GET', 'POST'])
def twittercharts_sums_per_timerange():

	print "From Facebook Charts. IP: "+str(request.remote_addr)

	template = "social_charts/twittercharts_sums_per_timerange.html"

	branches = get_branches()

	branch = request.form.get('branch')

	action = request.form.get('param')
	since = request.form.get('since')
	until = request.form.get('until')
	company = request.form.get('company')
	data = None

	if action:
		if not since or not until or str(since).strip()=='' or str(until).strip()=='':
			data = get_twitter_sums_per_timerange(company, None, None, branch)
		else:
			data = get_twitter_sums_per_timerange(company, since, until, branch)
	else:
		data = getTData("deletecompany")
		template="social_charts/twittermorechartsform.html"

	return render_template(template, branches=branches, qaction=action, tweets=data, since=since, until=until, msg="Give the dates (optional/experimental):", notlist=0, chart_type="twittercharts_sums_per_timerange", title="Companies sums per Time Range")





@app.route('/twittercharts_sums_per_weekday_weekend/', methods=['GET', 'POST'])
def twittercharts_sums_per_weekday_weekend():

	branches = get_branches()

	branch = request.form.get('branch')

	print "From Twitter Charts. IP: "+str(request.remote_addr)

	template = "social_charts/twittercharts_sums_per_weekday_weekend.html"

	action = request.form.get('param')
	since = request.form.get('since')
	until = request.form.get('until')
	company = request.form.get('company')
	data = None

	if action:
		if not since or not until or str(since).strip()=='' or str(until).strip()=='':
			data = get_twitter_sums_per_weekdays_weekends(company, None, None, branch)
		else:
			data = get_twitter_sums_per_weekdays_weekends(company, since, until, branch)
	else:
		data = getTData("deletecompany")
		template="social_charts/twittermorechartsform.html"

	# return render_template(template, tweets=data, title="Twitter Data Retrieval")
	return render_template(template, company=company, branches=branches, qaction=action, tweets=data, since=since, until=until, msg="Give the dates (optional/experimental):", notlist=0, chart_type="twittercharts_sums_per_weekday_weekend", title="Companies per weekday/weekend")





@app.route('/twittercharts_sums_per_char_range/', methods=['GET', 'POST'])
def twittercharts_sums_per_char_range():

	branches = get_branches()

	branch = request.form.get('branch')

	print "From Twitter Charts. IP: "+str(request.remote_addr)

	template = "social_charts/twittercharts_sums_per_char_range.html"

	action = request.form.get('param')
	since = request.form.get('since')
	until = request.form.get('until')
	company = request.form.get('company')
	data = None

	if action:
		if not since or not until or str(since).strip()=='' or str(until).strip()=='':
			data = get_twitter_sums_per_char_range(company, None, None, branch)
		else:
			data = get_twitter_sums_per_char_range(company, since, until, branch)
	else:
		data = getTData("deletecompany")
		template="social_charts/twittermorechartsform.html"

	# return render_template(template, tweets=data, title="Twitter Data Retrieval")
	return render_template(template, company=company, branches=branches, qaction=action, tweets=data, since=since, until=until, msg="Give the dates (optional/experimental):", notlist=0, chart_type="twittercharts_sums_per_char_range", title="Companies per character range")




############ GOOGLE PLUS ############
@app.route('/googleplusform/', methods=['GET', 'POST'])
def googleplusform():
	print "From Googel Plus. IP: "+str(request.remote_addr)

	branches = get_branches()

	if request.method == "POST":
		company = request.form['company']
		since = request.form['since']
		# until = request.form['until']

		branch = request.form['branch']

		delete = 1
		if request.form.get('nodelete') and request.form.get('nodelete')=='on':
			delete = 0

		if not since or str(since).strip()=='':
			flash("Please give the Since date ")
			return render_template("googleplusform.html", branches=branches)

		if company:
			print "From Google Plus. Company: "+company.strip()
			pluses=GooglePlusParser(company.strip(), since, delete, branch)
			return render_template("googleplus.html", pluses=pluses, title="Google+ Data Retrieval")
		else:
			flash("Please give a company name")
		# pass

	return render_template("googleplusform.html", branches=branches)



@app.route('/googleplusdataform/', methods=['GET', 'POST'])
def googleplusdataform():
	print "From GooglePlus data. IP: "+str(request.remote_addr)
	if request.method == "POST":

		company = request.form.get('company')
		since = request.form['since']
		until = request.form['until']

		# print "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
		# print company
		# print "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"

		if company:
			print "From GooglePlus data. IP: "+str(request.remote_addr)+" Company: "+company.strip()+", Since:"+ since +" Until:"+ until
			# fbs=FBParser([company.strip()], population)
			data, company_name, branch = get_googleplus_data(company.strip(), since, until)
			return render_template("googleplusdata.html", pluses=data, company=company, branch=branch, title="GooglePlus Data Retrieval")
		else:
			flash("Please give a company name")
		# pass

	data = getGPData("deletecompany")
	return render_template("googleplusdataform.html", gps=data)



@app.route('/deletegooglepluscompany/', methods=['GET', 'POST'])
def deleteGPcompany():
	company = request.args.get('company')

	if company:
		company = urllib.unquote(company)
		print "From Google+ Delete Company. IP: "+str(request.remote_addr)+" Company: "+company
		result = delete_existingGP(company)
		if int(result) >= 0:
			flash("Company %s deleted successfully!" % company)

	data = getGPData("deletecompany")
	return render_template("social_charts/googleplusdeletecompany.html", gps=data, title="Delete Google+ Company")









@app.route('/googlepluscharts/', methods=['GET', 'POST'])
def googlepluscharts():

	print "From Google+ Charts. IP: "+str(request.remote_addr)

	template = "social_charts/googlepluschartsform.html"

	options={
    "aggregate":"social_charts/googlepluscharts.html",
    "posts":"social_charts/googlepluspostscharts.html",
    "likes":"social_charts/googlepluslikescharts.html",
    "shares":"social_charts/googleplussharescharts.html",
    "deletecompany":"social_charts/googleplusdeletecompany.html"
	}

	action = request.form.get('param')
	since = request.form.get('since')
	until = request.form.get('until')
	data = None

	if action and action in options:
		print "From Google+ Charts. IP: "+str(request.remote_addr)+" Action: "+action+", Since:"+ since +" Until:"+ until
		template = options[action]
		if not since or not until or str(since).strip()=='' or str(until).strip()=='':
			flash("Please give the Since/Until dates ")
			return render_template("social_charts/googlepluschartsform.html", title="Google+ Data Retrieval")
		
		data = getGPChartData(action, since, until)

	return render_template(template, gps=data, since=since, until=until, title="Google+ Data Retrieval")








#####################################################################


@app.route('/twitter/<cname>/')
def twitter(cname):
	tweets=TwitterParser(cname)
	return render_template("twitter.html", tweets=tweets)


@app.errorhandler(404)
def page_not_found(e):
	# return("The page was not found but don't worry, there there, it will be ok, it will be ok!")
	return render_template("404.html")

@app.errorhandler(405)
def method_not_found(e):
	# return("The page was not found but don't worry, there there, it will be ok, it will be ok!")
	return render_template("405.html")

@app.errorhandler(500)
def method_not_found(e):
	# return("The page was not found but don't worry, there there, it will be ok, it will be ok!")
	return render_template("500.html")

@app.route('/trytest/')
def trytest():
	try:
		return render_template("facebook.html", TOPIC_DICT = TOPICS_DICT)
	except Exception, e:
		# raise
		# return(str(e))
		return render_template("500.html", exc=str(e))
	else:
		pass
	finally:
		pass


@app.route('/login/', methods=['GET', 'POST'])
def login_page():
	error = None
	try:
		if request.method == "POST":
			attempted_username = request.form['username']
			attempted_password = request.form['password']

			# flash(attempted_username)
			# flash(attempted_password)

			if attempted_username == "admin" and attempted_password == "password":
				return redirect(url_for('homepage'))
			else:
				error = "Invalid user/pass! Please retry!!!"

		return render_template("login.html", error=error)
		# pass


	except Exception, e:
		flash(e)
		return render_template("login.html", error=error)
	else:
		pass
	finally:
		pass

	return render_template("login.html")


class RegistrationForm(Form):
	username = TextField('Username', [validators.Length(min=4, max=20)])
	email = TextField('Email Address', [validators.Length(min=6, max=50)])
	password = PasswordField('Password', [validators.Required(), validators.EqualTo('confirm', message="Passwords must match...")])
	confirm = PasswordField('Repeat Password')
	accept_tos = BooleanField('I accept the <a href="/tos/">terms of service</a>', [validators.Required()])






@app.route('/register/', methods=["GET", "POST"])
def register_page():
	try:
		# c, conn = connection()
		# return("Connection was successful!!!")
		form = RegistrationForm(request.form)

		if request.method == "POST" and form.validate():
			username = form.username.data
			email = form.email.data
			password = sha256_crypt.encrypt(str(form.password.data))

			c, conn = connection()
			print thwart(username)

			x = c.execute("SELECT * FROM users WHERE username = (%s)", [thwart(username)])

			if int(x) > 0:
				flash("This username already exists!")
				return render_template('register.html', form=form)
			else:
				c.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
					       (thwart(username), thwart(password), thwart(email)  ))

				conn.commit()

				flash("Thank you for regstering")
				c.close()
				conn.close()

				gc.collect()

				session['logged_in'] = True
				session['username'] = username

				return redirect(url_for('register_page'))

		return render_template("register.html", form=form)




	except Exception as e:
		return(str(e))

if __name__ == "__main__":
	app.run(host = '0.0.0.0', debug=True)
