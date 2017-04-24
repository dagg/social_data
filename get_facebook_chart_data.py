from dbconnect import connection
# import itertools
import gc
import datetime

aggregatequery="select company, CAST(count(company) AS SIGNED) as posts, CAST(sum(likes) AS SIGNED) as total_likes, CAST(sum(shares) AS SIGNED) as total_shares, CAST(sum(comments) AS SIGNED) as total_comments from facebook group by company order by total_likes desc"
postsquery="select company, CAST(count(company) AS SIGNED) as posts from facebook group by company order by posts desc"
likesquery="select company, CAST(sum(likes) AS SIGNED) as total_likes from facebook group by company order by total_likes desc"
sharesquery="select company, CAST(sum(shares) AS SIGNED) as total_shares from facebook group by company order by total_shares desc"
commentsquery="select company, CAST(sum(comments) AS SIGNED) as total_comments from facebook group by company order by total_comments desc"
companiesquery="select distinct company, company_name from facebook order by company"


options={
    "aggregate":aggregatequery,
    "posts":postsquery,
    "shares":sharesquery,
    "likes":likesquery,
    "comments":commentsquery,
    "deletecompany":companiesquery
}

def getData(action):
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

    return data

def getChartData(action, since, until):

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

    caggregatequery="select company, CAST(count(company) AS SIGNED) as posts, CAST(sum(likes) AS SIGNED) as total_likes, CAST(sum(shares) AS SIGNED) as total_shares, CAST(sum(comments) AS SIGNED) as total_comments from facebook %s group by company order by total_likes desc" % (sinceuntilq)
    cpostsquery="select company, CAST(count(company) AS SIGNED) as posts from facebook %s group by company order by posts desc" % (sinceuntilq)
    clikesquery="select company, CAST(sum(likes) AS SIGNED) as total_likes from facebook %s group by company order by total_likes desc" % (sinceuntilq)
    csharesquery="select company, CAST(sum(shares) AS SIGNED) as total_shares from facebook %s group by company order by total_shares desc" % (sinceuntilq)
    ccommentsquery="select company, CAST(sum(comments) AS SIGNED) as total_comments from facebook %s group by company order by total_comments desc" % (sinceuntilq)

    coptions={
    "aggregate":caggregatequery,
    "posts":cpostsquery,
    "shares":csharesquery,
    "likes":clikesquery,
    "comments":ccommentsquery
    }


    c.execute(coptions[action])
    # data = list(itertools.chain.from_iterable(cursor))
    data = list(c.fetchall())
    c.close()
    conn.close()
    gc.collect()
    # print data

    return data


