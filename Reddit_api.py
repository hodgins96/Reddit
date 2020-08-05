import requests
import json

data = {'grant_type': 'password', 'username': 'vaxxine_search', 'password': 'Passcode1'}
auth = requests.auth.HTTPBasicAuth('tnR6JRMF8AnS-g','BDZJvrtYl4QyWt2DoaawfztVJUM')
r = requests.post('https://www.reddit.com/' + 'api/v1/access_token',
                  data=data,
                  headers={'user-agent': 'subreddit_search by vaxxine_search'},
		          auth=auth)
d = r.json()

token = d['access_token']

headers = {'Authorization': 'bearer ' + token, 'User-Agent': 'subreddit_search by vaxxine_search'}
search = {'q':'Meteor', 'limit': 100, 'show':'All','restrict_sr': True} #restric_sr restricts to that subreddit
req = requests.get('https://oauth.reddit.com/r/niagarafallsontario/search/', headers=headers, params=search)

results = req.json()

siblingPosts = results['data']['children']
print(json.dumps(results, indent=4, sort_keys=True))
# results = results['data']['children'][0]['data']
# title = results['title']
# print(json.dumps(results, indent=4, sort_keys=True))
title = []
link = []
#keys = siblingPosts[0]['data'].keys()
#print(keys)
# print(title)
pos = 0
for x in siblingPosts: # for loop for searching through multiple posts
    title.append(siblingPosts[pos]['data']['title'])
    link.append(siblingPosts[pos]['data']['permalink'])
    print(title[pos] + " Link " + "reddit.com" + link[pos])
    pos += 1


# TO DO 
# Comment code
# Figure out why results from other subreddits show up 
# Email returned information 
# Allow for custom inputs of subreddits and search terms

