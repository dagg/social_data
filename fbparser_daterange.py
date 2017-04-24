#!/usr/bin/python
# -*- coding: utf-8 -*-

# import sys, getopt
import urllib2
import json
import csv
import datetime
from dbconnect import connection
import gc


def delete_existing(company):
    c, conn = connection()

    conn.set_character_set('utf8')
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')
    c.execute("set session sql_mode='';")
    conn.commit()

    # first delete existing
    data = c.execute("delete from facebook where company = (%s)", [company])
    conn.commit()
    c.close()
    conn.close()
    gc.collect()
    return data

def db_insert(company, data):

    c, conn = connection()

    conn.set_character_set('utf8')
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')
    c.execute("set session sql_mode='';")
    conn.commit()

    # then insert new
    created = ''
    message = ''
    post_type = ''
    likes = None
    shares = None
    comments = None

    try:
        if data[3] and data[3].strip() is not '':
            created = data[3]
    except IndexError as e:
        print e

    try:
        if data[1] and data[1].strip() is not '':
            message = data[1]
    except IndexError as e:
        print e

    try:
        if data[2] and data[2].strip() is not '':
            post_type = data[2]
    except IndexError as e:
        print e

    try:
        if data[4] and data[4].strip() is not '':
            likes = data[4]
    except IndexError as e:
        print e

    try:
        if data[5] and data[5].strip() is not '':
            shares = data[5]
    except IndexError as e:
        print e

    try:
        if data[6] and data[6].strip() is not '':
            comments = data[6]
    except IndexError as e:
        print e

        
    query = "insert into facebook (company, created, message, type, likes, shares, comments) values (%s, %s, %s, %s, %s, %s, %s)"

    c.execute(query, (company, created, message.encode('utf-8'), post_type, likes, shares, comments))

    conn.commit()

    c.close()
    conn.close()
    gc.collect()



datetimeformat = '%Y-%m-%d %H:%M:%S'
datetimegreekformat = '%d-%m-%Y %H:%M:%S'

def render_to_json(graph_url):
    #render graph url call to JSON
    print graph_url+"\n"
    web_response = urllib2.urlopen(graph_url)
    readable_page = web_response.read()
    json_data = json.loads(readable_page)
    
    return json_data


def getFBposts(company, graphurl, since, until):
    graph_url = "https://graph.facebook.com/v2.5"
    if company and since and until:
        access_token="156677781373009|7303b3e525e283b63d026d817d96b3b6"
        test_url=graph_url+"/"+company+"/posts?fields=message%2Ccreated_time%2Clikes.limit(1).summary(true)%2Cshares%2Ccomments.limit(1).summary(true)%2Ctype&since="+since+"&until="+until+"&limit=10&access_token="+access_token
        json_postdata = render_to_json(test_url)
        return json_postdata
    elif company and graphurl:
        json_postdata = render_to_json(graphurl)
        return json_postdata
    else:
        return None
    
# def FBParser(companies, population):
def FBParser(companies, since, until):

    since = datetime.datetime.strptime(since, '%d/%m/%Y').strftime('%Y-%m-%d')
    until = datetime.datetime.strptime(until, '%d/%m/%Y').strftime('%Y-%m-%d')

    #simple data pull App Secret and App ID
    APP_ID="xxxxxxxxxxxxxxx"
    APP_SECRET="yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"
    access_token="xxxxxxxxxxxxxxx|yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"
    #to find go to page's FB page, at the end of URL find username
    #e.g. http://facebook.com/walmart, walmart is the username
    # list_companies = ["vodafonegreece", "cosmote"]
    list_companies = companies
    
    fblist=[]
    for company in list_companies:

        delete_existing(company)

        pages=[]

        #extract post data
        json_postdata = getFBposts(company, None, since, until)
        json_fbposts = json_postdata['data']

        pages.append(json_fbposts)

        c=0
        # while 'paging' in json_postdata and 'next' in json_postdata['paging'] and c< (int(int(population)/10)-1):
        while 'paging' in json_postdata and 'next' in json_postdata['paging']:
            nexturl = json_postdata['paging']['next']
            json_postdata = getFBposts(company, nexturl, None, None)
            json_fbposts = json_postdata['data']

            pages.append(json_fbposts)
            c=c+1
        
        
        #print post messages and ids
        for page in pages:
        # for post in json_fbposts:
            for post in page:
                fb=[]
                try:
                    #try to print out data
                    fb.append(post["id"])
                    fb.append(post["message"].strip().replace("\n", " - "))
                    fb.append(post["type"])
                    # fb.append( datetime.datetime.strftime(   datetime.datetime.strptime(post["created_time"].replace('+0000','').replace('T', ' '), datetimeformat), datetimegreekformat   ) )
                    fb.append( str(datetime.datetime.strptime(post["created_time"].replace('+0000','').replace('T', ' '), datetimeformat)) )

                    if "likes" in post:
                        if "summary" in post["likes"]:
                            fb.append(str(post["likes"]["summary"]["total_count"]))
                        else:
                            fb.append('')
                    else:
                        fb.append('')
                    
                    if "shares" in post:
                        if "count" in post["shares"]:
                            fb.append(str(post["shares"]["count"]))
                        else:
                            fb.append('')
                    else:
                        fb.append('')

                    if "comments" in post:
                        if "summary" in post["comments"]:
                            fb.append(str(post["comments"]["summary"]["total_count"]))
                        else:
                            fb.append('')
                    else:
                        fb.append('')
                            
                except Exception as e:
                     print "Key error:"+str(e)
                
                fblist.append(fb)
                db_insert(company, fb)
    return fblist
