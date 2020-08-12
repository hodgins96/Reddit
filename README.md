# Reddit
subreddit search

Small python script to search a subreddit for posts with a keyword or phrase inside the title filters all returned results if keyword/phrase doesnt exist in it.

Uses environment variables for all keys usernames and passwords, flags to allow the user to dictate which subreddit they want to search, what to search, and how many reuslts they want.

Example of flags python3 Reddit_api.py -s hockey -t salad -l 1
Or      python3 Reddit_api.py -subreddit hockey -term -limit 1

Emails send in HTML format but have a plain text backup 
sends email through gmail with SSL connection