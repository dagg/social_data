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

	return c, conn