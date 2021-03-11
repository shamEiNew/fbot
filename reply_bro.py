import tweepy
import logging
from os import environ
import time
import config


def reply_bro():
    api = config.create_api()
    for tweet in tweepy.Cursor(api.user_timeline, user_id = 67611162).items(2):
        try:
            api.update_status(
                status = tweet.text.encode('ascii','ignore').decode('utf-8') + " bro",
                in_reply_to_status_id=tweet.id,
                auto_populate_reply_metadata = True
                )
        except:
            pass