from time import sleep
import tweepy
from credentials import consumer_key, consumer_secret,\
    access_token, access_token_secret
from ceps import get_energy_for_now

def tram_equivalent(*args):
    tram_eqv = int(round(sum(args)/2.82*1000, 0))
    tram_eqv = list(str(tram_eqv).replace('.', ','))
    for i in range(1,len(tram_eqv)):
        if i % 3 == 0:
            tram_eqv.insert(i, ' ')
    return ''.join(tram_eqv)

if __name__ == '__main__':
    # Twitter app authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    
    while True:
        # Get energy generation data from CEPS
        solar = get_energy_for_now('FVE')
        wind = get_energy_for_now('VTE')
        
        # Prepare strings for the tweet
        tram = tram_equivalent(float(wind['value']), float(solar['value']))
        solar = str(solar['value']).replace('.', ',')
        wind = str(wind['value']).replace('.', ',')

        tweet = f"🌬️ {wind} MWh\n☀️ {solar} MWh\nběhem uplynulé hodiny.\n\nOdpovídá spotřebě jedné 🚋 při jízdě dlouhé {tram} km (2,82 kWh/km)."
        print(tweet)
        api.update_status(status=tweet)
        sleep(3600)
