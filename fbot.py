import tweepy
import logging
import time
from os import environ
import random as rn


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

consumer_key = environ['API_KEY']
consumer_secret = environ['API_SECRET_KEY']
access_token = environ['ACCESS_TOKEN']
access_token_secret = environ['ACESS_TOKEN_SECRET']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


try:
    api.verify_credentials()
except Exception as e:
    logger.error("Error creating API", exc_info=True)
    raise e

def check_mentions(api, since_id):
    quotes = open("quotes.txt", "r", encoding='utf-8')
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if follow_followers(api, api.get_status(tweet.id).user.screen_name) == True:
            try:
                logger.info(f"following {m}")
                api.create_friendship(m)
            except tweepy.TweepError:
                logger.info(f"you can't follow {m}!")

        if tweet.in_reply_to_status_id is not None:
            continue
        if api.me().screen_name not in prev_tweets(api, api.get_status(tweet.id).user.screen_name, str(tweet.id)):

            if api.get_status(tweet.id).user.id_str != '1164161687450112000':
                logger.info(f"Answering to {tweet.user.name}")
                try:
                    api.update_status(status="Humpty dumpty \U0001F970",
                     in_reply_to_status_id=tweet.id, auto_populate_reply_metadata = True)
                except tweepy.TweepError:
                    logger.error(f"status duplicate")
            else:
                logger.info(f"Answering to my user")
                try:
                    api.update_status(status=quotes.readlines()[rn.randint(0, len(quotes.readlines()))-1],
                    in_reply_to_status_id=tweet.id,auto_populate_reply_metadata = True)
                except tweepy.TweepError:
                    logger.error(f"status duplicate")
        m = ''
    quotes.close()
    return new_since_id

def prev_tweets(api, name, tweet_id):
    s = []
    for tweet in tweepy.Cursor(api.search,q='to:'+name, result_type='recent',
     timeout=999999).items():
        if hasattr(tweet, 'in_reply_to_status_id_str'):
            if (tweet.in_reply_to_status_id_str==tweet_id):
                status = api.get_status(int(tweet.id))
                s.append(status.user.screen_name)
    if not s:
        return [0,]
    return s

def follow_followers(api, m):
    if api.me().id not in api.followers_ids(m):
        return True

def mentions_main():
    since_id = 1
    while True:
        since_id = check_mentions(api, since_id)
        logger.info("Waiting...")
        time.sleep(60*2)

if (__name__ == "__main__"):
    api.rate_limit_status()
    mentions_main()