import tweepy
import logging
from os import environ
import time

def reply_bro(api, since_id, user):
    max_id = since_id
    for tweet in tweepy.Cursor(api.user_timeline, user_id = user, since_id = since_id).items(2):
        max_id = max(since_id, tweet.id)
        if tweet.in_reply_to_status_id is None:
            try:
                api.update_status(
                    status = tweet.text.encode('ascii','ignore').decode('utf-8') + " bro",
                    in_reply_to_status_id=tweet.id,
                    auto_populate_reply_metadata = True
                    )
            except:
                pass
    return max_id