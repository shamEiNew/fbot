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
        since_id=since_id).items(10):
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        logger.info(f"Answering to {tweet.user.name}")
        print(prev_tweets(api, tweet.user.name, tweet.id))
        if api.me().name in prev_tweets(api, tweet.user.name, tweet.id):
            api.update_status(
                status="u are absoluteyly amazing \U0001F970",
                in_reply_to_status_id=tweet.id, auto_populate_reply_metadata = True
                )
    return new_since_id

def prev_tweets(api, name, tweet_id):
    replies=[]
    for tweet in tweepy.Cursor(api.search,q='to:'+name, result_type='recent', timeout=999999).items(50):
        if tweet.in_reply_to_status_id is not None:
            if (tweet.in_reply_to_status_id_str==tweet_id):
                replies.append(tweet.user.name)
    return replies

def mentions_main():
    api = create_api()
    since_id = 1
    while True:
        since_id = check_mentions(api, since_id)
        logger.info("Main Mentions Waiting...")
        time.sleep(15)

if (__name__ == "__main__"):
    mentions_main()