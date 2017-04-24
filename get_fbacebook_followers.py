import urllib2
import json

def render_to_json(graph_url):
    #render graph url call to JSON
    print graph_url+"\n"
    web_response = urllib2.urlopen(graph_url)
    readable_page = web_response.read()
    json_data = json.loads(readable_page)
    
    return json_data


def getFBfollowers(company):
    graph_url = "https://graph.facebook.com/v2.5"
    if company:
        access_token="xxxxxxxxxxxxxxx|yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"

        test_url=graph_url+"/"+company+"?fields=name,likes&access_token="+access_token
        json_postdata = render_to_json(test_url)
        return json_postdata
    elif company and graphurl:
        json_postdata = render_to_json(graphurl)
        return json_postdata
    else:
        return None

def FB_Followers_parser(company):
    json_postdata = getFBfollowers(company)
    # json_fbposts = json_postdata['posts']['data']

    followers=json_postdata['likes']
    company_name=json_postdata['name']

    return company, company_name, followers

# Example:
# print FB_Followers_parser('vodafonegreece')
