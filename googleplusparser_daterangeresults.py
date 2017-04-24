from apiclient.discovery import build
import datetime
import time
from dbconnect import connection
import gc


def delete_existingGP(company):
    c, conn = connection()

    conn.set_character_set('utf8')
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')
    c.execute("set session sql_mode='';")
    conn.commit()

    query = "delete from googleplus where company = '%s'" % company

    # first delete existing
    data = c.execute(query)
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
    name = ''
    content = ''
    post_type = ''
    likes = None
    shares = None
    comments = None
    company_code = ''

    try:
        if data[0] and data[0].strip() is not '':
            created = data[0]
    except IndexError as e:
        print e

    try:
        if data[7] and data[7].strip() is not '':
            name = data[7]
    except IndexError as e:
        print e

    try:
        if data[6] and data[6].strip() is not '':
            content = data[6]
    except IndexError as e:
        print e

    try:
        if data[5] and data[5].strip() is not '':
            post_type = data[5]
    except IndexError as e:
        print e

    try:
        if data[3] and data[3] is not '':
            likes = data[3]
    except IndexError as e:
        print e

    try:
        if data[4] and data[4] is not '':
            shares = data[4]
    except IndexError as e:
        print e

    try:
        if data[2] and data[2] is not '':
            comments = data[2]
    except IndexError as e:
        print e

    try:
        if data[8] and data[8].strip() is not '':
            company_code = data[8]
    except IndexError as e:
        print e

    query = "insert into googleplus (company, company_code, created, name, content, type, likes, shares, comments, branch_id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    c.execute(query, (company, company_code, created, name.encode('utf-8'), content.encode('utf-8'), post_type, likes, shares, comments, branch))

    conn.commit()

    c.close()
    conn.close()
    gc.collect()






def GooglePlusParser(company, since, delete, branch):

    # since='01/02/2016'
    # until='20/03/2016'
    until = time.strftime("%d/%m/%Y")

    startDate = datetime.datetime.strptime(since, '%d/%m/%Y').strftime('%Y-%m-%d')
    startDate = datetime.datetime.strptime(startDate, '%Y-%m-%d')
    endDate = datetime.datetime.strptime(until, '%d/%m/%Y').strftime('%Y-%m-%d')
    endDate = datetime.datetime.strptime(endDate, '%Y-%m-%d')

    # API_KEY = "xxxxxxxxxxxx_yyyyyyyyyyyyyyyyyyyyyyyyyy"# copied from project credentials page
    API_KEY = "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
    MAX_RESULTS = 200

    service = build('plus', 'v1', developerKey=API_KEY)
    activity_feed = service.activities().list(userId=company, collection="public", maxResults=20)
    # items = activity_feed.execute().get('items', [])

    activity_results = []

    activity_date=endDate


    if delete==1:
        delete_existingGP(company)

    # while activity_feed != None and len(activity_results) < MAX_RESULTS:
    while activity_feed != None and activity_date > startDate:

        
        activities = activity_feed.execute()

        if 'items' in activities:

            for activity in activities['items']:

                activity_date= datetime.datetime.strptime(activity["published"].split('T')[0], '%Y-%m-%d')

                company_code = activity['actor']['displayName']
                replies=0
                plusoners=0
                resharers=0
                objectType=''
                displayName=''
                content=''

                if "attachments" in activity["object"]:
                    if len(activity["object"]["attachments"])>0:
                        objectType=activity["object"]["attachments"][0]["objectType"]
                        if "displayName" in activity["object"]["attachments"][0]:
                            displayName=activity["object"]["attachments"][0]["displayName"].encode("utf-8").decode("utf-8")
                        # if "content" in activity["object"]["attachments"][0]:
                        #     content=activity["object"]["attachments"][0]["content"].encode("utf-8").decode("utf-8") 
                        if "title" in activity:
                            content=activity["title"].encode("utf-8").decode("utf-8") 

                if activity["object"]["replies"]["totalItems"]:
                    replies = activity["object"]["replies"]["totalItems"]

                if activity["object"]["plusoners"]["totalItems"]:
                    plusoners = activity["object"]["plusoners"]["totalItems"]

                if activity["object"]["resharers"]["totalItems"]:
                    resharers = activity["object"]["resharers"]["totalItems"]


                gp=[
                    activity["published"].split('T')[0]+" "+activity["published"].split('T')[1][:-1], 
                    activity["updated"], 

                    replies,
                    plusoners,
                    resharers,
                    objectType, 
                    displayName, 
                    content,
                    company_code
                    ]

                activity_results.extend([gp])

                db_insert(company, gp, branch)

                activity_feed = service.activities().list_next(activity_feed, activities)


    return activity_results


# Example:
# print GooglePlusParser('+vodafonegr')
