import tweepy
import credentials

consumer_key = credentials.API_KEY
consumer_secret_key = credentials.API_SECRET_KEY
access_token = credentials.ACCESS_TOKEN
access_token_secret = credentials.ACCESS_TOKEN_SECRET

auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

if __name__ == "__main__":
    api.update_status("I'm happy")