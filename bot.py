import tweepy
from credentials import consumer_key, consumer_secret,\
    access_token, access_token_secret
from ceps import get_energy_for_now
from entsoe import get_past_hour_energy, default_params


if __name__ == '__main__':
    # Twitter app authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    
    # Tweet generation data from entsoe unless past hour is missing
    try:
        solar = get_past_hour_energy('Solar', default_params)
        wind = get_past_hour_energy('Wind Onshore', default_params)
        biomass = get_past_hour_energy('Biomass', default_params)
        water = get_past_hour_energy('Hydro Run-of-river and poundage', default_params)

        tweet = f"🌬️ {wind} MWh\n" + \
                f"☀️ {solar} MWh\n" + \
                f"🌿 {biomass} MWh\n" + \
                f"💧 {water} MWh\n" + \
                "obnovitelné ⚡ během uplynulé hodiny"
        api.update_status(status=tweet)
    except IndexError:
        pass
