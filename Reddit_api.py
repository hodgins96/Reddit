import requests
import json
from email.message import EmailMessage
import smtplib
import os #environment variables
from datetime import datetime
#func get_token
b_url = 'https://www.reddit.com/'
reddit_name = os.environ.get('REDDIT_NAME')
reddit_pass = os.environ.get('REDDIT_PASS')
reddit_public = os.environ.get('REDDIT_PUBLIC')
reddit_private = os.environ.get('REDDIT_PRIVATE')
#environment _variables next two lines
data = {'grant_type': 'password', 'username': reddit_name, 'password': reddit_pass}
auth = requests.auth.HTTPBasicAuth(reddit_public,reddit_private)
r = requests.post(b_url + 'api/v1/access_token',
                  data=data,
                  headers={'user-agent': 'subreddit_search by vaxxine_search'},
		          auth=auth)
d = r.json()

token = d['access_token']
 
#func call api / dissect api 
db_url = 'https://oauth.reddit.com/r/' #url called once token is recieved
option = '/search' #for future so can be easily changed
subreddit = 'BuyCanadian'
search_term = 'Beer'
headers = {'Authorization': 'bearer ' + token, 'User-Agent': 'subreddit_search by vaxxine_search'}
search = {'q':search_term, 'limit': 100,'restrict_sr': True} #restric_sr restricts to that subreddit
req = requests.get(db_url + subreddit + option, headers=headers, params=search)

results = req.json()

siblingPosts = results['data']['children'] #how many posts are found
#print(json.dumps(results, indent=4, sort_keys=True))
# results = results['data']['children'][0]['data']
# title = results['title']
print(json.dumps(results, indent=4, sort_keys=True))
title = [] #Refactor into Dictionary????
link = []
selfText = []
date = []
thumbnail = []
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
            selfText.append('None')
        else:
            first25 = siblingPosts[pos]['data']['selftext']
            if(len(first25) > 100 ):
                selfText.append(first25[:100]+'... Continued through link') #first one hundred characters otherwise some posts are massive
            else:
                selfText.append(first25)
            #selfText.append('True')
        date.append(datetime.utcfromtimestamp(siblingPosts[pos]['data']['created_utc']))
        thumbnail.append(siblingPosts[pos]['data']['thumbnail'])
            
    pos+=1  
print(date[0])
count = 0
content = 'Results returned from search \n\n'
htmlContent = '<html> \n <h1>Results returned from search </h1> \n <body> \n <p> \n '
for ele in title:
    content = content + ('Post:' + str(count + 1) +" "+ ele +"\nLink: "+b_url +link[count]  + "\n" + "Time Posted: " + str(date[count]) + " utc \n" "Post Text: " + selfText[count] + "\n\n")
    htmlContent = htmlContent + ('<h3>Post: ' + str(count + 1) +' '+ ele +'</h3>Link: '+b_url + link[count]  + '<br>'+"Time Posted: "+ str(date[count])+ ' utc <br>' + 'Post Text: ' + selfText[count]  + '<br>' + '<img src="' + thumbnail[count] + '"alt="Thumbnail Not Available" class="center"/> <br><br>')
    count +=1
#func send email 
htmlContent = htmlContent + "</p> \n </body> \n </html>"
to = 'redditsearch.bot@gmail.com'
#environment Variable
sender = os.environ.get('EMAIL_ACC')
#Environment variable
pwd = os.environ.get('EMAIL_PASS')

msg = EmailMessage()
msg['Subject'] = f'Search Results for {search_term} in /r/{subreddit}' #fstring for ease
msg['From'] = sender
msg['To'] = to

msg.set_content(content) #Make email content message above in for loop
msg.add_alternative(htmlContent,subtype='html')
try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender,pwd)
    server.send_message(msg)
    server.quit()
except Exception as e:
    print("Your Princess is in another castle")
    print(e)





# TO DO 
# Comment code
# Python Flags, Regex?, Clean up and refactor code 
# Allow for custom inputs of subreddits and search terms

