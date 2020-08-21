import tweepy
import logging
import credentials

logger = logging.getLogger()

def create_api():
    consumer_key = credentials.API_KEY
    consumer_secret = credentials.API_SECRET_KEY
    access_token = credentials.ACCESS_TOKEN
    access_token_secret = credentials.ACCESS_TOKEN_SECRET

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api
