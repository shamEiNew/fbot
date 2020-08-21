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
        logger.info(f"Answering to {tweet.user.name}")
        api.update_status(
                status="forever u too \U0001F970",
                in_reply_to_status_id=tweet.id, auto_populate_reply_metadata = True
                )
    return new_since_id

def check_mentions_target(api, keywords, since_id):
    logger.info("Retrieving mentions by target")
    new_since_id = since_id
    target_user = credentials.USER_TW_ID
    for tweet in tweepy.Cursor(api.user_timeline, id = target_user,
        since_id=since_id).items(10):
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        if any(keyword in tweet.text.lower() for keyword in keywords):
            logger.info(f"Answering to {tweet.user.name}")

            if not tweet.user.following:
                tweet.user.follow()

            api.update_status(
                status="good",
                in_reply_to_status_id=tweet.id, auto_populate_reply_metadata = True
            )
    return new_since_id



def mentions_main():
    api = create_api()
    since_id = 1
    while True:
        since_id = check_mentions(api, since_id)
        logger.info("Main Mentions Waiting...")

def mentions_target():
    api = create_api()
    since_id = 1
    while True:
        since_id = check_mentions_target(api,["amz"], since_id)
        logger.info("Mentions target Waiting...")
        time.sleep(86400)

if __name__ == "__main__":
    mentions_main()
    mentions_target()
