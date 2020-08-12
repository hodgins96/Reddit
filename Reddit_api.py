import requests 
import json
from email.message import EmailMessage #email
import smtplib #email
import os #environment variables
from datetime import datetime
import argparse #flag arguments

def get_token(): #gets oath authenticarion token
    b_url = 'https://www.reddit.com/'
    reddit_name = os.environ.get('REDDIT_NAME')
    reddit_pass = os.environ.get('REDDIT_PASS')
    reddit_public = os.environ.get('REDDIT_PUBLIC')
    reddit_private = os.environ.get('REDDIT_PRIVATE')
    #environment _variables next two lines
    data = {'grant_type': 'password', 'username': reddit_name, 'password': reddit_pass}
    auth = requests.auth.HTTPBasicAuth(reddit_public,reddit_private)
    response = requests.post(b_url + 'api/v1/access_token',
                    data=data,
                    headers={'user-agent': 'subreddit_search by vaxxine_search'},
                    auth=auth)
    access_token = response.json()

    token = access_token['access_token']
    return token

def send_email(filtered_results,subreddit,search_term): #send emails
    count = 0
    url = 'https://www.reddit.com'
    content = 'Results returned from search \n\n'
    htmlContent = '<html> \n <h1>Results returned from search </h1> \n <body> \n <p> \n '
    for ele in filtered_results:
        content = content + ('Post:' + str(count + 1) +' '+ ele['Title'] +'\nLink: '+ url + ele['Link']  + '\n' + 'Time Posted: ' + str(ele['Date']) + ' utc \n' 'Post Text: ' + ele['Selftext'] + '\n\n')
        htmlContent = htmlContent + ('<h3>Post: ' + str(count + 1) +' '+ ele['Title'] +'</h3><b>Link:</b> '+url + ele['Link']  + '<br>'+'<b>Time Posted: </b>'+ str(ele['Date']) + ' utc <br>' + '<b>Post Text: </b>' + ele['Selftext']  + '<br>' + '<img src="' + ele['Thumbnail'] + '"alt="Thumbnail Not Available" class="center"/> <br><br>')
        count +=1

    htmlContent = htmlContent + '</p> \n </body> \n </html>'
    to = 'redditsearch.bot@gmail.com' #change to careers@vaxxine.com
    #environment Variable
    sender = os.environ.get('EMAIL_ACC')
    #Environment variable
    pwd = os.environ.get('EMAIL_PASS')

    msg = EmailMessage()
    msg['Subject'] = f'Search Results for {search_term} in /r/{subreddit}' #fstring for ease
    msg['From'] = sender
    msg['To'] = to

    msg.set_content(content) #sets content for plain text email
    msg.add_alternative(htmlContent,subtype='html') #sets content for html
    try: #try except incase server is funny
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465) #used a gmail 
        server.login(sender,pwd)
        server.send_message(msg)
        server.quit()
    except Exception as exception: 
        print(exception)

#func call api / dissect api needs args and token
def api_call_filter(token,subreddit,search_term,limit):

    db_url = 'https://oauth.reddit.com/r/' #url after oath setup
    option = '/search' #for future so can be easily changed
    if subreddit == None: #if not argument passed manually set
        subreddit = 'Hockey'
    if search_term == None:
        search_term = 'New York Rangers'
    if limit == None: #same check as above
        limit = 100
    headers = {'Authorization': 'bearer ' + token, 'User-Agent': 'subreddit_search by vaxxine_search'}
    search = {'q':search_term, 'limit': limit,'restrict_sr': True} #restric_sr restricts to that subreddit
    req = requests.get(db_url + subreddit + option, headers=headers, params=search)

    results = req.json() #results returned from get request

    siblingPosts = results['data']['children'] #how many posts are found
    filtered_results = [] #kist to add dictionary into it
    pos = 0
    for x in siblingPosts: # for loop for searching through multiple posts
        if search_term.casefold() in siblingPosts[pos]['data']['title'].casefold(): #casefold to check for work matching not case
            if(siblingPosts[pos]['data']['selftext'])=="": #if theres no self text add a message saying so
                dict ={'Title':siblingPosts[pos]['data']['title'],'Link':siblingPosts[pos]['data']['permalink'],'Selftext':'No Post Body','Date':datetime.utcfromtimestamp(siblingPosts[pos]['data']['created_utc']),'Thumbnail':siblingPosts[pos]['data']['thumbnail']}
                filtered_results.append(dict)
            elif len(siblingPosts[pos]['data']['selftext']) > 250: #limits post text to 250 charachters
            #some posts consume to much screen when not limited
                dict ={'Title':siblingPosts[pos]['data']['title'],'Link':siblingPosts[pos]['data']['permalink'],'Selftext':siblingPosts[pos]['data']['selftext'][0:250],'Date':datetime.utcfromtimestamp(siblingPosts[pos]['data']['created_utc']),'Thumbnail':siblingPosts[pos]['data']['thumbnail']}
                filtered_results.append(dict)
            else:
                dict ={'Title':siblingPosts[pos]['data']['title'],'Link':siblingPosts[pos]['data']['permalink'],'Selftext':siblingPosts[pos]['data']['selftext'],'Date':datetime.utcfromtimestamp(siblingPosts[pos]['data']['created_utc']),'Thumbnail':siblingPosts[pos]['data']['thumbnail']}
                filtered_results.append(dict)
        pos+=1 
    send_email(filtered_results,subreddit,search_term)
    



def main():
    api_call_filter(get_token(),args.subreddit,args.term,args.limit)
    #just calling this function beacuse flow control is staright forward
    


if __name__ == '__main__': #So can be used in future projects 
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--subreddit',help='Subreddit to search', action='store')
    parser.add_argument('-t','--term',help='Search term', action='store')
    parser.add_argument('-l','--limit',help='limit the amount of posts returned',action='store',type=int)
    args = parser.parse_args()
    main()

