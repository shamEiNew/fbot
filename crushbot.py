import tweepy
import logging
from config import create_api
import time
import credentials
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def follow_followers(api):
    logger.info("Retrieving and following followers")
    if api.me().id not in api.followers_ids("ubermensch_here"):
        logger.info("Following")
        try:
            api.create_friendship("ubermensch_here")
        except:
            logger.info("you can't follow your self!")

            
def main():
    api = create_api()
    #while True:
    follow_followers(api)
        #logger.info("Follower Waiting...")
        #time.sleep(60)
    print(type(api.followers((api.get_status(1296990480698232832)).user.screen_name)))
    print(True)

if __name__ == "__main__":
    main()