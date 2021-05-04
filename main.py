import time

from flask import Flask
import tweepy

import twetter_api_info


API_KEY = twetter_api_info.API_KEY
API_SECRET = twetter_api_info.API_SECRET
ACCESS_TOKEN = twetter_api_info.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = twetter_api_info.ACCESS_TOKEN_SECRET

app = Flask(__name__)

class AuthInfo(object):
    def __init__(self):
        self.auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
        self.auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


class TweetStream(tweepy.StreamListener):
    def __init__(self, api=None):
        self.auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
        self.auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.api = api
        self.first_connect = True

    def on_status(self, tweet):
        if self.first_connect:
            time.sleep(10)
            self.first_connect = False
        print(tweet.text)
        print(tweet.created_at)
        print(tweet.user.screen_name)


@app.route('/')
def main():
    auth = AuthInfo()
    tweet_stream = TweetStream(tweepy.API(auth.auth))
    stream = tweepy.Stream(auth=tweet_stream.api.auth, listener=tweet_stream)
    keyword = input()
    stream.filter(track=[keyword])


if __name__ == '__main__':
    app.run()


