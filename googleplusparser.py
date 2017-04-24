from apiclient.discovery import build


def GooglePlusParser(company):

	# API_KEY = "xxxxxxxxxxxx_yyyyyyyyyyyyyyyyyyyyyyyyyy"# copied from project credentials page
	API_KEY = "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
	GPLUS = build('plus', 'v1', developerKey=API_KEY)
	items = GPLUS.activities().list(userId=company, collection="public", maxResults=100).execute().get('items', [])

	pluses = []

	for item in items:

		replies=''
		plusoners=''
		resharers=''
		objectType=''
		displayName=''
		content=''

		if "attachments" in item["object"]:
			if len(item["object"]["attachments"])>0:
				objectType=item["object"]["attachments"][0]["objectType"]
				if "displayName" in item["object"]["attachments"][0]:
					displayName=item["object"]["attachments"][0]["displayName"].encode("utf-8").decode("utf-8")
				if "content" in item["object"]["attachments"][0]:
					content=item["object"]["attachments"][0]["content"].encode("utf-8").decode("utf-8") 


		pluses.extend([[
			item["published"], 
			item["updated"], 
			item["object"]["replies"]["totalItems"], 
			item["object"]["plusoners"]["totalItems"], 
			item["object"]["resharers"]["totalItems"], 
			objectType, 
			displayName, 
			content 
			]])

	return pluses

