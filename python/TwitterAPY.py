import requests
from requests.exceptions import ChunkedEncodingError, ConnectionError
from time import time, sleep

class page:
    """
    A page contains properties for the tweets in it,
    (one page always contains 10-500 tweets,
    depending on the max_result parameter in the request),
    for the users returned by the request,
    as well as the places and referenced tweets.
    """
    def __init__(self, data, endpoint):
        self._data = data
        self.endpoint = endpoint
        
    @property
    def tweets(self):
        if self.endpoint == 'fullarchivesearch':
            if self._data.get('data'):
                return [tweet(tweet_data) for tweet_data in self._data['data']]
            else:
                return None
    @property
    def users(self):
        if self.endpoint == 'fullarchivesearch':
            if self._data.get('includes'):
                if self._data['includes'].get('users'):
                    return [user(user_data) for user_data in self._data['includes']['users']]
                else:
                    return None
            else:
                return None
        elif self.endpoint == 'userfollowing' or self.endpoint == 'userfollowers':
            if self._data.get('data'):
                return [user(user_data) for user_data in self._data['data']]
            else:
                return None
    @property
    def places(self):
        if self._data.get('includes'):
            if self._data['includes'].get('places'):
                return [place(place_data) for place_data in self._data['includes']['places']]
            else:
                return None
        else:
            return None
    @property
    def referenced_tweets(self):
        if self._data.get('includes'):
            if self._data['includes'].get('tweets'):
                return [tweet(tweet_data) for tweet_data in self._data['includes']['tweets']]
            else:
                return None
        else:
            return None
    @property
    def next_token(self):
        if self._data.get('meta'):
            return self._data['meta'].get('next_token')
        else:
            return None

class tweet:
    def __init__(self,data):
        self._data = data
    
    @property
    def id(self):
        return self._data.get('id')
    @property
    def text(self):
        return self._data.get('text')
    @property
    def attachments(self):
        return self._data.get('attachments')
    @property
    def author_id(self):
        return self._data.get('author_id')
    @property
    def context_annotations(self):
        return self._data.get('context_annotations')
    @property
    def conversation_id(self):
        return self._data.get('conversation_id')
    @property
    def created_at(self):
        return self._data.get('created_at')
    @property
    def entities(self):
        return self._data.get('entities')
    @property
    def geo(self):
        return self._data.get('geo')
    @property
    def in_reply_to_user_id(self):
        return self._data.get('in_reply_to_user_id')
    @property
    def lang(self):
        return self._data.get('lang')
    @property
    def retweet_count(self):
        if 'public_metrics' in self._data.keys():
            return self._data['public_metrics'].get('retweet_count')
        else:
            return None
    @property
    def reply_count(self):
        if 'public_metrics' in self._data.keys():
            return self._data['public_metrics'].get('reply_count')
        else:
            return None
    @property
    def like_count(self):
        if 'public_metrics' in self._data.keys():
            return self._data['public_metrics'].get('like_count')
        else:
            return None
    @property
    def quote_count(self):
        if 'public_metrics' in self._data.keys():
            return self._data['public_metrics'].get('quote_count')
        else:
            return None
    @property
    def referenced_tweets(self):
        return self._data.get('referenced_tweets')
    @property
    def source(self):
        return self._data.get('source')
    @property
    def withheld(self):
        return self._data.get('withheld')
    @property
    def is_retweet(self):
        if self.referenced_tweets is not None:
            return any([(tweet.get('type') == 'retweeted') for tweet in self.referenced_tweets])
        else:
            return False
    @property
    def is_quote(self):
        if self.referenced_tweets is not None:
            return any([(tweet.get('type') == 'quoted') for tweet in self.referenced_tweets])
        else:
            return False
    @property
    def is_reply(self):
        if self.referenced_tweets is not None:
            return any([(tweet.get('type') == 'replied_to') for tweet in self.referenced_tweets])
        else:
            return False

class user:
    def __init__(self,data):
        self._data = data
    
    @property
    def id(self):
        return self._data.get('id')
    @property
    def name(self):
        return self._data.get('name')
    @property
    def username(self):
        return self._data.get('username')
    @property
    def created_at(self):
        return self._data.get('created_at')
    @property
    def description(self):
        return self._data.get('description')
    @property
    def entities(self):
        return self._data.get('entities')
    @property
    def location(self):
        return self._data.get('location')
    @property
    def pinned_tweet_id(self):
        return self._data.get('pinned_tweet_id')
    @property
    def pinned_tweet_id(self):
        return self._data.get('pinned_tweet_id')
    @property
    def profile_image_url(self):
        return self._data.get('profile_image_url')
    @property
    def protected(self):
        return self._data.get('protected')
    @property
    def followers_count(self):
        if 'public_metrics' in self._data.keys():
            return self._data['public_metrics'].get('followers_count')
        else:
            return None
    @property
    def following_count(self):
        if 'public_metrics' in self._data.keys():
            return self._data['public_metrics'].get('following_count')
        else:
            return None  
    @property
    def tweet_count(self):
        if 'public_metrics' in self._data.keys():
            return self._data['public_metrics'].get('tweet_count')
        else:
            return None
    @property
    def listed_count(self):
        if 'public_metrics' in self._data.keys():
            return self._data['public_metrics'].get('listed_count')
        else:
            return None
    @property
    def name(self):
        return self._data.get('name')
    @property
    def url(self):
        return self._data.get('url')
    @property
    def verified(self):
        return self._data.get('verified')
    @property
    def withheld(self):
        return self._data.get('withheld')    

class place:
    def __init__(self,data):
        self._data = data

    @property
    def id(self):
        return self._data.get('id')
    @property
    def full_name(self):
        return self._data.get('full_name')
    @property
    def country(self):
        return self._data.get('country')
    @property
    def country_code(self):
        return self._data.get('country_code')
    @property
    def geo(self):
        return self._data.get('geo')
    @property
    def name(self):
        return self._data.get('name')
    @property
    def place_type(self):
        return self._data.get('place_type')

#TODO more detailed query terms
class api:
    #user input of BearerToken
    def __init__(self,token,tweet_fields=['id','text','author_id','context_annotations','conversation_id','created_at','geo','lang','public_metrics','referenced_tweets','source'],
                 user_fields=['id','name','username','created_at','description','location','protected','public_metrics'],place_fields=['full_name','id','country','country_code','geo','name','place_type'],
                 tweet_expansions=['author_id','referenced_tweets.id','geo.place_id']):
        
        self.allowed_tweet_fields = ['id','text','attachments','author_id','context_annotations','conversation_id','created_at','entities','geo','in_reply_to_user_id','lang','public_metrics','referenced_tweets','source','withheld']
        self.allowed_user_fields = ['id','name','username','created_at','description','entities','location','pinned_tweet_id','profile_image_url','protected','public_metrics','url','verified','withheld']
        self.allowed_place_fields = ['full_name','id','contained_id','country','country_code','geo','name','place_type']
        self.allowed_tweet_expansions=['author_id','referenced_tweets.id','in_reply_to_user_id','attachments.media_keys','attachments.poll_ids','geo.place_id','entities.mentions.username','referenced_tweets.id.author_id']
        
        if any([field not in self.allowed_tweet_fields for field in tweet_fields]):
            raise TwitterAPYError('410','{} not allowed. Allowed fields are {}.'.format(tweet_fields, self.allowed_tweet_fields))
        if any([field not in self.allowed_user_fields for field in user_fields]):
            raise TwitterAPYError('410','{} not allowed. Allowed fields are {}.'.format(user_fields, self.allowed_user_fields))
        if any([field not in self.allowed_place_fields for field in place_fields]):
            raise TwitterAPYError('410','{} not allowed. Allowed fields are {}.'.format(place_fields, self.allowed_place_fields))
        if any([expansion not in self.allowed_tweet_expansions for expansion in tweet_expansions]):
            raise TwitterAPYError('410','{} not allowed. Allowed fields are {}.'.format(tweet_expansions, self.allowed_tweet_expansions))
        self.token = token
        self.tweet_fields = tweet_fields
        self.user_fields = user_fields
        self.tweet_expansions = tweet_expansions
        self.place_fields = place_fields

    def __build_headers__(self):
        headers = {"Authorization": "Bearer {}".format(self.token)}
        return headers

    def __build_params__(self,query):
        if self.endpoint_name =='fullarchivesearch':
            query['place.fields'] = ','.join(self.place_fields)
            query['expansions'] = ','.join(self.tweet_expansions)
        query['user.fields'] = ','.join(self.user_fields) 
        query['tweet.fields'] = ','.join(self.tweet_fields)
        return query
    
    def __check_rate_limit__(self, response):
        remaining = int(response.headers.get('x-rate-limit-remaining'))
        if remaining < 1:
            time_until_ratelimit = max(1,int(response.headers.get('x-rate-limit-reset')) - int(time()))
            print('Rate limit reached. Sleeping for {} and retrying again.'.format(time_until_ratelimit))
            sleep(time_until_ratelimit)
    
    def __handle_status__(self,response):
        #sleeps a second because of twitter limit to 1 request per second
        sleep(1)
        if response.status_code == 200:
            return True
        if response.status_code in [400,401,403,404]:
            raise TwitterAPYError(response.status_code, response.text)
        if response.status_code == 429:
            time_until_ratelimit = max(1,int(response.headers.get('x-rate-limit-reset')) - int(time()))
            print('Rate limit reached. Sleeping for {} and retrying again.'.format(time_until_ratelimit))
            sleep(time_until_ratelimit)
            return False
        if response.status_code >= 500:
            print('Error on Twitter side. Sleeping for {} and retrying again.'.format(60))
            sleep(60)
            return False
    
    def __handle_errors__(self,error,endpoint,headers,params):
        print("An unexpected error occured: {}./n Sleeping 60 seconds and retrying once.".format(str(type(error))))
        sleep(60)
        return requests.request("GET", endpoint, headers=headers, params=params)


    def full_archive_search(self,query,max_pages=False):
        self.endpoint_name = 'fullarchivesearch'
        endpoint = "https://api.twitter.com/2/tweets/search/all"
        headers = self.__build_headers__()
        params = self.__build_params__(query)
        pages = []
        success = False
        while not success:
            try:
                response = requests.request("GET", endpoint, headers=headers, params=params)
            except (ChunkedEncodingError,ConnectionError) as e:
                response = self.__handle_errors__(e,endpoint,headers,params)
            success = self.__handle_status__(response)
            if success:
                p = page(response.json(),self.endpoint_name)
                pages.append(p)
                while (p.next_token is not None) & (max_pages==False or len(pages)<max_pages):
                    self.__check_rate_limit__(response)
                    success_subsequent = False
                    while not success_subsequent:
                        params['next_token'] = p.next_token
                        try:
                            response = requests.request("GET", endpoint, headers=headers, params=params)
                        except (ChunkedEncodingError,ConnectionError) as e:
                            response = self.__handle_errors__(e,endpoint,headers,params)
                        success_subsequent = self.__handle_status__(response)
                        if success_subsequent:
                            p = page(response.json(),self.endpoint_name)
                            pages.append(p)
        return pages

    def user_following(self,user_id,query,max_pages=False):
        self.endpoint_name = 'userfollowing'
        endpoint = "https://api.twitter.com/2/users/{}/following".format(user_id)
        headers = self.__build_headers__()
        params = self.__build_params__(query)
        pages = []
        success = False
        while not success:
            try:
                response = requests.request("GET", endpoint, headers=headers, params=params)
            except (ChunkedEncodingError,ConnectionError) as e:
                response = self.__handle_errors__(e,endpoint,headers,params)
            success = self.__handle_status__(response)
            if success:
                p = page(response.json(),self.endpoint_name)
                pages.append(p)
                while (p.next_token is not None) & (max_pages==False or len(pages)<max_pages):
                    self.__check_rate_limit__(response)
                    success_subsequent = False
                    while not success_subsequent:
                        params['pagination_token'] = p.next_token
                        try:
                            response = requests.request("GET", endpoint, headers=headers, params=params)
                        except (ChunkedEncodingError,ConnectionError) as e:
                            response = self.__handle_errors__(e,endpoint,headers,params)
                        success_subsequent = self.__handle_status__(response)
                        if success_subsequent:
                            p = page(response.json(),self.endpoint_name)
                            pages.append(p)
        return pages

    def user_followers(self,user_id,query,max_pages=False):
        self.endpoint_name = 'userfollowers'
        endpoint = "https://api.twitter.com/2/users/{}/followers".format(user_id)
        headers = self.__build_headers__()
        params = self.__build_params__(query)
        pages = []
        success = False

        while not success:
            try:
                response = requests.request("GET", endpoint, headers=headers, params=params)
            except (ChunkedEncodingError,ConnectionError) as e:
                response = self.__handle_errors__(e,endpoint,headers,params)
            success = self.__handle_status__(response)
            if success:
                p = page(response.json(),self.endpoint_name)
                pages.append(p)
                while (p.next_token is not None) & (max_pages==False or len(pages)<max_pages):
                    self.__check_rate_limit__(response)
                    success_subsequent = False
                    while not success_subsequent:
                        params['pagination_token'] = p.next_token
                        try:
                            response = requests.request("GET", endpoint, headers=headers, params=params)
                        except (ChunkedEncodingError,ConnectionError) as e:
                            response = self.__handle_errors__(e,endpoint,headers,params)
                        success_subsequent = self.__handle_status__(response)
                        if success_subsequent:
                            p = page(response.json(),self.endpoint_name)
                            pages.append(p)
        return pages

class TwitterAPYError(Exception):
    def __init__(self, id, message):
        self.id = id
        self.message = message