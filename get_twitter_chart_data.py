from dbconnect import connection
# import itertools
import gc
import datetime

aggregatequery="select company, CAST(count(company) AS SIGNED) as posts, CAST(sum(favorites) AS SIGNED) as total_favorites, CAST(sum(retweets) AS SIGNED) as total_retweets from twitter group by company order by total_favorites"
postsquery="select company, CAST(count(company) AS SIGNED) as posts from twitter group by company"
favoritesquery="select company, CAST(sum(favorites) AS SIGNED) as total_favorites from twitter group by company"
retweetsquery="select company, CAST(sum(retweets) AS SIGNED) as total_retweets from twitter group by company"
companiesquery="select distinct company from twitter order by company"


options={
    "aggregate":aggregatequery,
    "posts":postsquery,
    "favorites":favoritesquery,
    "retweets":retweetsquery,
    "deletecompany":companiesquery
}

def getTData(action):
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

def getTChartData(action, since, until):

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

    caggregatequery="select company, CAST(count(company) AS SIGNED) as posts, CAST(sum(favorites) AS SIGNED) as total_favorites, CAST(sum(retweets) AS SIGNED) as total_retweets from twitter %s group by company order by total_favorites desc" % (sinceuntilq)
    cpostsquery="select company, CAST(count(company) AS SIGNED) as posts from twitter %s group by company order by posts desc" % (sinceuntilq)
    cfavoritesquery="select company, CAST(sum(favorites) AS SIGNED) as total_favorites from twitter %s group by company order by total_favorites desc" % (sinceuntilq)
    cretweetsquery="select company, CAST(sum(retweets) AS SIGNED) as total_retweets from twitter %s group by company order by total_retweets desc" % (sinceuntilq)
    
    coptions={
    "aggregate":caggregatequery,
    "posts":cpostsquery,
    "favorites":cfavoritesquery,
    "retweets":cretweetsquery
    }

    c.execute(coptions[action])
    # data = list(itertools.chain.from_iterable(cursor))
    data = list(c.fetchall())
    c.close()
    conn.close()
    gc.collect()
    # print data

    return data

