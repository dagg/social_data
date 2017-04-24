#!/usr/bin/env python

from apiclient.discovery import build

TMPL = '''
    published: %s
    updated: %s
    replies: %s
    plusoners: %s
    resharers: %s
'''

API_KEY = "xxxxxxxxxxxx_yyyyyyyyyyyyyyyyyyyyyyyyyy" # copied from project credentials page
GPLUS = build('plus', 'v1', developerKey=API_KEY)
items = GPLUS.activities().list(userId='+vodafonegr', collection="public").execute().get('items', [])

for item in items:
	print item["object"]["attachments"][0]["displayName"].encode("utf-8").decode("utf-8")
