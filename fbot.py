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

def check_mentions(api, keywords, since_id, T):
    try:
        quotes = open("quotes.txt", "r", encoding='utf-8')
    except FileNotFoundError as fr:
        logger.error("File Doesn't Exist")
        raise fr
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():
        #try:
        #    api.create_favorite(tweet.id)
        #except tweepy.error.TweepError:
        #    logger.error(f"Already favorited",exc_info=True)
        #    print('Already Liked')
        new_since_id = max(tweet.id, new_since_id)
        if follow_followers(api, api.get_status(tweet.id).user.screen_name) == True:
            m = api.get_status(tweet.id).user.screen_name
            try:
                logger.info(f"following {tweet.user.name}")
                api.create_friendship(m)
            except tweepy.TweepError:
                logger.error(f"you can't follow {tweet.user.name}!")

        if tweet.in_reply_to_status_id is not None:
            continue
        if api.me().screen_name not in prev_tweets(api, api.get_status(tweet.id).user.screen_name, str(tweet.id)):
            if api.get_status(tweet.id).user.id_str != environ['MY_USER']:
                logger.info(f"Answering to {tweet.user.name}")
                if any(keyword in tweet.text.lower() for keyword in keywords) == False:
                    try:
                        T += 1
                        api.update_status(status=str(T) + "Humpty dumpty",
                        in_reply_to_status_id=tweet.id, auto_populate_reply_metadata = True)
                    except tweepy.TweepError:
                        logger.error(f"status duplicate ---01")
                else:
                    try:
                        T += 1
                        api.update_status(status=str(T)+"  "+rej[rn.randint(0, len(rej))]  , in_reply_to_status_id=tweet.id, auto_populate_reply_metadata = True)
                    except:
                        logger.error(f"status duplicate ---02")
            else:
                
                logger.info(f"Answering to my user")
                try:
                    T += 1
                    api.update_status(status= "Hi! yup you're my crush. " + quotes.readlines()[rn.randint(0, len(quotes.readlines()))-1],
                    in_reply_to_status_id=tweet.id,auto_populate_reply_metadata = True)
                except tweepy.TweepError:
                    logger.error(f"status duplicate ---03")
        m = ''
    try:
        quotes.close()
    except:
        print('file not found')

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
    since_id = 1
    T = 0
    while True:
        since_id, T = check_mentions(api, ['are you my crush','you my crush','crush','who is your crush','crushh', 'whos your crush'],since_id, T)
        logger.info("Waiting...")
        time.sleep(60*60*12)

if (__name__ == "__main__"):
    rej = ["you beautiful but no \U0001F60D", "may be next time \U0000263A", "There can be only one, sorry",
     "Nope", "Noooope","Hi but nayyy","nayyyyyy", "I would have but one at a time \U0001F92A"]
    time = time.asctime()
    try:
        api.update_status("(^_^) still single now too......(^_^) "+ str(rn.randint(1, 500)))
    except:
        logger.info('Status duplicate ---04')
    mentions_main()