import urllib2
import json

def render_to_json(graph_url):
    #render graph url call to JSON
    print graph_url
    web_response = urllib2.urlopen(graph_url)
    readable_page = web_response.read()
    json_data = json.loads(readable_page)
    
    return json_data


def getFBposts(company, graphurl):
    graph_url = "https://graph.facebook.com/v2.5"
    if graphurl:
        json_postdata = render_to_json(graphurl)
        # json_fbposts = json_postdata['data']
        return json_postdata
    else:
        if company:
            access_token="xxxxxxxxxxxxxxx|yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"
            test_url=graph_url+"/"+company+"/posts?fields=message%2Ccreated_time%2Clikes.limit(1).summary(true)%2Cshares%2Ccomments.limit(1).summary(true)%2Ctype&limit=10&access_token="+access_token
            json_postdata = render_to_json(test_url)
            # json_fbposts = json_postdata['data']
            return json_postdata
        else:
            return None

    
def FBParser(companies, population):
    #simple data pull App Secret and App ID
    APP_ID="xxxxxxxxxxxxxxx"
    APP_SECRET="yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"

    access_token="xxxxxxxxxxxxxxx|yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"
    #to find go to page's FB page, at the end of URL find username
    #e.g. http://facebook.com/walmart, walmart is the username
    # list_companies = ["vodafonegreece", "cosmote"]
    list_companies = companies
    # graph_url = "https://graph.facebook.com/v2.5"
    
    fblist=[]
    for company in list_companies:
        #make graph api url with company username

        # test_url=graph_url+"/"+company+"/posts?fields=message%2Ccreated_time%2Clikes%2Cshares%2Ccomments%2Ctype&limit=100&access_token="+access_token
        # test_url=graph_url+"/"+company+"/posts?fields=message%2Ccreated_time%2Clikes%2Cshares%2Ccomments%2Ctype&limit=100&access_token="+access_token

        pages=[]

        #extract post data
        # json_postdata = render_to_json(test_url)
        json_postdata = getFBposts(company, None)
        json_fbposts = json_postdata['data']

        pages.append(json_fbposts)

        c=0
        while 'paging' in json_postdata and 'next' in json_postdata['paging'] and c< (int(int(population)/10)-1):
            nexturl = json_postdata['paging']['next']
            json_postdata = getFBposts(company, nexturl)
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
                    # print "ID: "+post["id"]
                    fb.append(post["id"])
                    # print "MESSAGE: "+post["message"].strip().replace("\n", " - ")
                    fb.append(post["message"].strip().replace("\n", " - "))
                    # print "TYPE: "+post["type"]
                    fb.append(post["type"])
                    # print "DATETIME: "+post["created_time"]
                    fb.append(post["created_time"])
                    # print "LIKES: "+str(len(post["likes"]["data"]))
                    if "likes" in post:
                        if "summary" in post["likes"]:
                            fb.append(str(post["likes"]["summary"]["total_count"]))
                        else:
                            fb.append('')
                    else:
                        fb.append('')
                    # print "SHARES: "+str(post["shares"]["count"])
                    fb.append(str(post["shares"]["count"]))
                    # print "COMMENTS: "+str(len(post["comments"]["data"]))
                    if "comments" in post:
                        if "summary" in post["comments"]:
                            fb.append(str(post["comments"]["summary"]["total_count"]))
                        else:
                            fb.append('')
                    else:
                        fb.append('')
                            
                    
                except Exception:
    #                print "Key error:"+post["story"]
                     # print "ID: "+post["id"]
                     print "Key error:"
                
                fblist.append(fb)
            
        #print the data we pulled
        # print page_data
    return fblist

# if __name__ == "__main__":
#     main()    
