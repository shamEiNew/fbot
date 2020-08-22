import tweepy
import logging
from config import create_api
import time
import credentials

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def check_mentions(api, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        if api.me().screen_name not in prev_tweets(api, api.get_status(tweet.id).user.screen_name, str(tweet.id)):
            logger.info(f"Answering to {tweet.user.name}")
            api.update_status(status="u are absolutely amazing \U0001F970", in_reply_to_status_id=tweet.id, auto_populate_reply_metadata = True)
    return new_since_id

def prev_tweets(api, name, tweet_id):
    s = []
    for tweet in tweepy.Cursor(api.search,q='to:'+name, result_type='recent', timeout=999999).items(5):
        #print(type(tweet))
        if hasattr(tweet, 'in_reply_to_status_id_str'):
            if (tweet.in_reply_to_status_id_str==tweet_id):
                status = api.get_status(int(tweet.id))
                s.append(status.user.screen_name)
    if not s:
        return [0,]
    return s

def mentions_main():
    api = create_api()
    since_id = 1
    while True:
        since_id = check_mentions(api, since_id)
        logger.info("Main Mentions Waiting...")
        time.sleep(15)

if (__name__ == "__main__"):
    mentions_main()