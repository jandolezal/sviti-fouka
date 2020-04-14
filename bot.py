import tweepy
from credentials import consumer_key, consumer_secret,\
    access_token, access_token_secret
from ceps import get_energy_for_now

if __name__ == '__main__':
    # Twitter app authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    
    # Get energy generation data from CEPS
    solar = get_energy_for_now('FVE')
    wind = get_energy_for_now('VTE')
    
    # Prepare strings for the tweet
    solar = str(solar['value']).replace('.', ',')
    wind = str(wind['value']).replace('.', ',')

    tweet = f"🌬️ {wind} MWh\n☀️ {solar} MWh\nběhem uplynulé hodiny."
    api.update_status(status=tweet)
