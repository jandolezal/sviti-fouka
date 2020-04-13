import tweepy
from credentials import consumer_key, consumer_secret,\
    access_token, access_token_secret
from ceps import get_energy_for_now

def tram_equivalent(*args):
    tram_eqv = int(round(sum(args)/2.82*1000, 0))
    tram_eqv = str(tram_eqv).replace('.', ',')
    return tram_eqv

if __name__ == '__main__':
    under_construction = True
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    
    if not under_construction:
        solar = get_energy_for_now('FVE')
        wind = get_energy_for_now('VTE')
    solar = {'value': '500.0'}
    wind = {'value': '250.0'}
    
    tram = tram_equivalent(float(wind['value']), float(solar['value']))
    solar = str(solar['value']).replace('.', ',')
    wind = str(wind['value']).replace('.', ',')

    tweet = f"🌬️ {wind} MWh\n☀️ {solar} MWh\n\n🚋{tram} km"
    api.update_status(status=tweet)
