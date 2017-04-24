from dbconnect import connection
# import itertools
import gc
import datetime

aggregatequery="select company_code, CAST(count(company_code) AS SIGNED) as posts, CAST(sum(likes) AS SIGNED) as total_likes, CAST(sum(shares) AS SIGNED) as total_shares from googleplus group by company_code order by total_likes desc"
postsquery="select company_code, CAST(count(company_code) AS SIGNED) as posts from googleplus group by company_code order by posts desc"
likesquery="select company_code, CAST(sum(favorites) AS SIGNED) as total_favorites from googleplus group by company_code order by total_favorites desc"
sharesquery="select company_code, CAST(sum(retweets) AS SIGNED) as total_retweets from googleplus group by company_code order by total_retweets desc"

companiesquery="select distinct company, company_code from googleplus order by company"


options={
    "aggregate":aggregatequery,
    "posts":postsquery,
    "likes":likesquery,
    "shares":sharesquery,
    "deletecompany":companiesquery
}

def getGPData(action):
    c, conn = connection()

    conn.set_character_set('utf8')
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')
    c.execute("set session sql_mode='';")
    conn.commit()

    c.execute(options[action])
    # data = list(itertools.chain.from_iterable(cursor))
    data = list(c.fetchall())
    c.close()
    conn.close()
    gc.collect()
    # print data

    return data

def getGPChartData(action, since, until):

    since = datetime.datetime.strptime(since, '%d/%m/%Y').strftime('%Y-%m-%d')
    until = datetime.datetime.strptime(until, '%d/%m/%Y').strftime('%Y-%m-%d')



    c, conn = connection()

    conn.set_character_set('utf8')
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')
    c.execute("set session sql_mode='';")
    conn.commit()

    sinceuntilq=" where created >= '%s' and created <= '%s'" % (since, until)

    caggregatequery="select company_code, CAST(count(company_code) AS SIGNED) as posts, CAST(sum(likes) AS SIGNED) as total_likes, CAST(sum(shares) AS SIGNED) as total_shares from googleplus %s group by company_code order by total_likes desc" % (sinceuntilq)
    cpostsquery="select company_code, CAST(count(company_code) AS SIGNED) as posts from googleplus %s group by company_code" % (sinceuntilq)
    clikesquery="select company_code, CAST(sum(likes) AS SIGNED) as total_likes from googleplus %s group by company_code" % (sinceuntilq)
    csharesquery="select company_code, CAST(sum(shares) AS SIGNED) as total_shares from googleplus %s group by company_code" % (sinceuntilq)
    
    coptions={
    "aggregate":caggregatequery,
    "posts":cpostsquery,
    "likes":clikesquery,
    "shares":csharesquery
    }


    c.execute(coptions[action])
    # data = list(itertools.chain.from_iterable(cursor))
    data = list(c.fetchall())
    c.close()
    conn.close()
    gc.collect()
    # print data

    return data

