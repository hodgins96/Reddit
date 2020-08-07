import requests
import json
#func get_token
b_url = 'https://www.reddit.com/'
data = {'grant_type': 'password', 'username': 'vaxxine_search', 'password': 'Passcode1'}
auth = requests.auth.HTTPBasicAuth('tnR6JRMF8AnS-g','BDZJvrtYl4QyWt2DoaawfztVJUM')
r = requests.post(b_url + 'api/v1/access_token',
                  data=data,
                  headers={'user-agent': 'subreddit_search by vaxxine_search'},
		          auth=auth)
d = r.json()

token = d['access_token']
 
#func call api / dissect api 
db_url = 'https://oauth.reddit.com/r/' #url called once token is recieved
option = '/search' #for future so can be easily changed
subreddit = 'hockey'
search_term = 'salad'
headers = {'Authorization': 'bearer ' + token, 'User-Agent': 'subreddit_search by vaxxine_search'}
search = {'q':search_term, 'limit': 25,'restrict_sr': True} #restric_sr restricts to that subreddit
req = requests.get(db_url + subreddit + option, headers=headers, params=search)

results = req.json()

siblingPosts = results['data']['children'] #how many posts are found
#print(json.dumps(results, indent=4, sort_keys=True))
# results = results['data']['children'][0]['data']
# title = results['title']
print(json.dumps(results, indent=4, sort_keys=True))
title = []
link = []
selfText = []
#keys = siblingPosts[0]['data'].keys()
#print(keys)
# print(title)
pos = 0
for x in siblingPosts: # for loop for searching through multiple posts
    #print(siblingPosts[pos]['data']['title'])
    #print(siblingPosts[pos]['data']['permalink'])
    #print(siblingPosts[pos]['data']['selftext'])
    if search_term.casefold() in siblingPosts[pos]['data']['title'].casefold(): #casefold to check for work matching not case

        title.append(siblingPosts[pos]['data']['title'])
        link.append(siblingPosts[pos]['data']['permalink'])
        if(siblingPosts[pos]['data']['selftext'])=="":
            selfText.append('No Self Text')
        else:
            selfText.append(siblingPosts[pos]['data']['selftext'])
            
            
        #print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    pos+=1  
count = 0
for ele in title:
    print('Post :) ' + str(count + 1) +" "+ ele + link[count]  + "\n")
    count +=1
#func send email 




# TO DO 
# Comment code
# Figure out why results from other subreddits show up 
# Email returned information 
# Allow for custom inputs of subreddits and search terms

