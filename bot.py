import tweepy
from credentials import consumer_key, consumer_secret,\
    access_token, access_token_secret


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

tweet = '''🌬️ 📈 128,6 MWh\n
☀️ 📈 624,5 MWh\n\n
🚋 267 057 km
'''

api.update_status(status=tweet)
