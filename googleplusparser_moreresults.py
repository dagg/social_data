from apiclient.discovery import build


def GooglePlusParser(company):

	# API_KEY = "xxxxxxxxxxxx_yyyyyyyyyyyyyyyyyyyyyyyyyy"# copied from project credentials page
	API_KEY = "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
	MAX_RESULTS = 200

	service = build('plus', 'v1', developerKey=API_KEY)
	activity_feed = service.activities().list(userId=company, collection="public", maxResults=100)
	# items = activity_feed.execute().get('items', [])

	activity_results = []

	while activity_feed != None and len(activity_results) < MAX_RESULTS:
		
		activities = activity_feed.execute()

		if 'items' in activities:

			for activity in activities['items']:

				replies=''
				plusoners=''
				resharers=''
				objectType=''
				displayName=''
				content=''

				if "attachments" in activity["object"]:
					if len(activity["object"]["attachments"])>0:
						objectType=activity["object"]["attachments"][0]["objectType"]
						if "displayName" in activity["object"]["attachments"][0]:
							displayName=activity["object"]["attachments"][0]["displayName"].encode("utf-8").decode("utf-8")
						if "content" in activity["object"]["attachments"][0]:
							content=activity["object"]["attachments"][0]["content"].encode("utf-8").decode("utf-8") 


				activity_results.extend([[
					activity["published"], 
					activity["updated"], 
					activity["object"]["replies"]["totalItems"], 
					activity["object"]["plusoners"]["totalItems"], 
					activity["object"]["resharers"]["totalItems"], 
					objectType, 
					displayName, 
					content 
					]])

				activity_feed = service.activities().list_next(activity_feed, activities)

	return activity_results


# Example:
# print GooglePlusParser('+vodafonegr')
