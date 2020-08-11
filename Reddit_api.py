import requests
import json
from email.message import EmailMessage
import smtplib
import os #environment variables
from datetime import datetime
#Use arg parse for flags
#func get_token returns token
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
access_token = r.json()

token = access_token['access_token']
 
#func call api / dissect api needs args and token
db_url = 'https://oauth.reddit.com/r/' #url called once token is recieved
option = '/search' #for future so can be easily changed
subreddit = 'BuyCanadian'
search_term = 'Beer'
headers = {'Authorization': 'bearer ' + token, 'User-Agent': 'subreddit_search by vaxxine_search'}
search = {'q':search_term, 'limit': 100,'restrict_sr': True} #restric_sr restricts to that subreddit
req = requests.get(db_url + subreddit + option, headers=headers, params=search)

results = req.json()

siblingPosts = results['data']['children'] #how many posts are found
print(json.dumps(results, indent=4, sort_keys=True))
filtered_results = []
pos = 0
for x in siblingPosts: # for loop for searching through multiple posts
    if search_term.casefold() in siblingPosts[pos]['data']['title'].casefold(): #casefold to check for work matching not case
        if(siblingPosts[pos]['data']['selftext'])=="":
            dict ={'Title':siblingPosts[pos]['data']['title'],'Link':siblingPosts[pos]['data']['permalink'],'Selftext':'No Post Body','Date':datetime.utcfromtimestamp(siblingPosts[pos]['data']['created_utc']),'Thumbnail':siblingPosts[pos]['data']['thumbnail']}
            filtered_results.append(dict)
        else:
            dict ={'Title':siblingPosts[pos]['data']['title'],'Link':siblingPosts[pos]['data']['permalink'],'Selftext':siblingPosts[pos]['data']['selftext'],'Date':datetime.utcfromtimestamp(siblingPosts[pos]['data']['created_utc']),'Thumbnail':siblingPosts[pos]['data']['thumbnail']}
            filtered_results.append(dict)
            
    pos+=1 
#func send email takes in list of dictionary

count = 0
content = 'Results returned from search \n\n'
htmlContent = '<html> \n <h1>Results returned from search </h1> \n <body> \n <p> \n '
for ele in filtered_results:
    content = content + ('Post:' + str(count + 1) +" "+ ele['Title'] +"\nLink: "+b_url + ele['Link']  + "\n" + "Time Posted: " + str(ele['Date']) + " utc \n" "Post Text: " + ele['Selftext'] + "\n\n")
    htmlContent = htmlContent + ('<h3>Post: ' + str(count + 1) +' '+ ele['Title'] +'</h3><b>Link:</b> '+b_url + ele['Link']  + '<br>'+"<b>Time Posted: </b>"+ str(ele['Date']) + ' utc <br>' + '<b>Post Text: </b>' + ele['Selftext']  + '<br>' + '<img src="' + ele['Thumbnail'] + '"alt="Thumbnail Not Available" class="center"/> <br><br>')
    count +=1

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


#if __name__ == '__main__': if imported to another class


# TO DO 
# Comment code
# Python Flags(Arg_parse), Clean up and refactor code 

