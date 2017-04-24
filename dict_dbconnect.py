import MySQLdb
# import MySQLdb.cursors
from dbdetails import DBDetails

DB_Details = DBDetails()

def connection():
	conn = MySQLdb.connect(host=DB_Details["host"], 
		                   user=DB_Details["user"],
		                   passwd=DB_Details["passwd"],
		                   db=DB_Details["db"],
		                   # cursorclass=MySQLdb.cursors.DictCursor
		                   )
	c=conn.cursor()
	cdict = conn.cursor(MySQLdb.cursors.DictCursor)

	return c, conn, cdict


# example query using the dict cursor
# 
# cursor = conn.cursor(MySQLdb.cursors.DictCursor)
# cursor.execute("SELECT name, category FROM animal")
# result_set = cursor.fetchall()
# for row in result_set:
#     print "%s, %s" % (row["name"], row["category"])