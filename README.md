# Reddit
subreddit search

Small python (3.82) script to search a subreddit for posts with a keyword or phrase inside the title filters all returned results if keyword/phrase doesnt exist in it.

Uses environment variables for all keys usernames and passwords, flags to allow the user to dictate which subreddit they want to search, what to search, and how many reuslts they want.

Example of flags python3 Reddit_api.py -s hockey -t salad -l 1
Or      python3 Reddit_api.py -subreddit hockey -term salad -limit 1 /n

if arguments are not passed in it will use set ones
if multiple search terms use ' '
        python3 Reddit_api.py -subreddit aww -term 'orange cat' -limit 1

Emails send in HTML format with thumbnails when available but have a plain text backup 
sends email through gmail with SSL connection
