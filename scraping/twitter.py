# library needed to access twitter
import tweepy as tw
from datetime import datetime

# standard django library required
from .models import Tweet
from celery import shared_task

# library needed to read the twitter API keys from file
import configparser

def search_tweets(keywords):
    parser = configparser.ConfigParser()
    parser.read("config.ini")
    CONSUMER_KEY = parser.get('twitter', 'CONSUMER_KEY')
    CONSUMER_SECRET = parser.get('twitter', 'CONSUMER_SECRET')
    ACCESS_TOKEN = parser.get('twitter', 'ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = parser.get('twitter', 'ACCESS_TOKEN_SECRET')

    # consumer-key, consumer-secret    
    auth = tw.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    # access token, access-token secret
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tw.API(auth)
    # Define the search term and the date_since date as variables
    # use filter to avoid searching for retweets
    search_words = "#spacex" + " -filter:retweets"
    now = datetime.now() # current date and time
    date_since = now.strftime("%Y-%m-%d")
    tweets = tw.Cursor(api.search,
                q=search_words,
                lang="en",
                since=date_since).items(20)
    return tweets

@shared_task
def store_tweets():
    original_tweets = search_tweets('')
    for original_tweet in original_tweets:
        if not Tweet.objects.filter(tweet_id = original_tweet.id):
            print('Adding new tweet')
            tweet_id_type = type(original_tweet.id)
            dtime = original_tweet.created_at
            new_datetime = datetime.strftime(dtime, '%Y-%m-%d %H:%M:%S')
            new_tweet = Tweet.objects.create(tweet_id = original_tweet.id, txt = original_tweet.text, published_date = new_datetime, is_active = True)
