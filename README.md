# TwitterAPY
A slim python wrapper for the twitter academic API.

# Installation
Currently there is no simple way to install the wrapper. Simply clone the git and place the TwitterAPY.py file into the directory you are working with.

# Working with the wrapper
Start by initializing the API:
```api = TwitterAPY.api('YOUR_BEARER_TOKEN')
```
The wrapper then offers currently three functions.
Full Archive Search:
```pages = api.full_archive_search(query,max_pages=False)
```
max_pages can take any int value and will only collect this many pages from twitter.
query is a standard twitter api query, see e.g. https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query. the query parameter also allows other information to be passed such as max_results. In this case it should be a dictionary containing the query parameter.
The users a user is following:
```pages = user_following(user_id,query,max_pages=False)
```
here user_id is the id of the user for which you want to collect the accounts she follows.
The users that are following a user:
```	pages = user_followers(user_id,query,max_pages=False)
```
each of these functions returns a list of page objects. Each object has properties that return the tweets, users, etc. that are saved on a page.

Simple working example:
```
api = TwitterAPY.api('YOUR_BEARER_TOKEN')
query = {'query':'(happy OR happiness) lang:en','max_results':10}
pages = api.full_archive_search(query,max_pages=2)
for page in pages:
	for tweet in page.tweets:
		print('{}: {}'.format(tweet.id, tweet.text))
```
# Advantages
The wrapper automatically handles the twitter rate limits and adds a standard set of fields to all data collected. This can be adjusted when calling the api object.