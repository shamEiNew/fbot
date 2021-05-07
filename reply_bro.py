import tweepy
import logging
from os import environ
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def reply_bro(api, user, text):
    api.send_direct_message(user, text)