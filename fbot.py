import tweepy
import logging
import time
from os import environ
import random as rn
import datetime
import music_recommend as mr

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
def create_api():
    consumer_key = environ['API_KEY']
    consumer_secret = environ['API_SECRET_KEY']
    access_token = environ['ACCESS_TOKEN']
    access_token_secret = environ['ACCESS_TOKEN_SECRET']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api

def check_mentions(api, keywords, since_id, T):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():
        """try:
           api.create_favorite(tweet.id)
        except tweepy.error.TweepError:
           logger.error(f"Already favorited",exc_info=True)
           print('Already Liked')"""
        new_since_id = max(tweet.id, new_since_id)
        if follow_followers(api, api.get_status(tweet.id).user.screen_name) == True:
            try:
                logger.info(f"following {tweet.user.name}")
                api.create_friendship(api.get_status(tweet.id).user.screen_name)
            except tweepy.TweepError:
                logger.error(f"you can't follow {tweet.user.name}!")

        if tweet.in_reply_to_status_id is not None:
            continue
        if api.me().screen_name not in prev_tweets(api,api.get_status(tweet.id).user.screen_name, str(tweet.id)):
            if api.get_status(tweet.id).user.id_str != environ['MY_USER']:
                logger.info(f"Answering to {tweet.user.name}")
                if any(keyword in tweet.text.lower() for keyword in keywords) == False:
                    try:
                        T += 1
                        api.update_status(status=str(T) + " Humpty dumpty",
                        in_reply_to_status_id=tweet.id, auto_populate_reply_metadata = True)
                    except tweepy.TweepError:
                        logger.error(f"status duplicate ---01")
                else:
                    try:
                        T += 1
                        api.update_status(status=str(T)+"  :sowwwwyyy I give songs to only my fav person as of now \U0001F605 yikes!!!"+"  "+ rej[rn.randint(0, len(rej)-1)]  , in_reply_to_status_id=tweet.id, auto_populate_reply_metadata = True)
                    except:
                        logger.error(f"status duplicate for different user")
            else:
                if '\u2764\ufe0f' in tweet.text and len(tweet.text.encode('ascii','ignore').decode('utf-8').replace('@TheCrushBot','').strip())>0:
                    try:
                        logger.info(f"Answering to my user: a music")
                        api.update_status(status = "A song for you {name} \n {song_link}".format(name=tweet.user.name,
                        song_link = mr.song_pub(tweet.text.encode('ascii','ignore').decode('utf-8').replace('@TheCrushBot','').replace('\U00002764','').strip())),
                        in_reply_to_status_id = tweet.id, auto_populate_reply_metadata=True)
                    except:
                        logger.info(f'Status duplicate for my user: music')
                else:
                    try:
                        logger.info(f"Answering to my user: a reply")
                        T += 1
                        api.update_status(status= "luv u \U00002764 " + quotes_list[rn.randint(0, len(quotes_list)-1)],
                        in_reply_to_status_id=tweet.id,auto_populate_reply_metadata = True)
                    except tweepy.TweepError:
                        logger.error(f"status duplicate for my user: reply")
    return new_since_id, T

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
    api = create_api()
    since_id = 1
    T = 0
    while True:
        since_id, T = check_mentions(api, ['are you my crush','you my crush','crush','who is your crush','crushh', 'whos your crush'],since_id, T)
        logger.info("Waiting...")
        time.sleep(60*60*12)

if (__name__ == "__main__"):
    rej = ["you beautiful but no \U0001F60D", "may be next time \U0000263A", "There can be only one, sorry","Nope", "Noooope","Hi but nayyy","nayyyyyy", "I would have but one at a time \U0001F92A"]
    
    try:
        quotes = open("quotes.txt", "r", encoding='utf-8')
    except FileNotFoundError as fr:
        logger.error("File Doesn't Exist")
        raise fr
    quotes_list = quotes.readlines()
    quotes.close()
    
    mentions_main()