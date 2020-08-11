import os
import datetime
from entsoe import get_renewable_energy, url, params, res_map
from dotenv import load_dotenv
import tweepy

if __name__ == '__main__':
    load_dotenv()

    # Get energy from past hour. Script will be a cron job run at HH:05
    start = (datetime.datetime.utcnow() - datetime.timedelta(hours=1)).isoformat(timespec='hours')
    end = datetime.datetime.utcnow().isoformat(timespec='hours')
    past_hour = start + '%2F' + end

    # Update params to make a Entsoe API request
    params['securityToken'] = os.getenv('ENTSOE_TOKEN')
    params['TimeInterval'] = past_hour

    #Get energy for past hour from Entsoe API
    energy = get_renewable_energy(url, params, res_map)

    # Twitter app authentication
    consumer_key = os.getenv('CONSUMER_KEY')
    consumer_secret = os.getenv('CONSUMER_SECRET')
    access_token = os.getenv('ACCESS_TOKEN')
    access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    
    # Tweet the data
    tweet = f"🌬️ {energy['Wind Onshore']} MWh\n" + \
            f"☀️ {energy['Solar']} MWh\n" + \
            f"🌿 {energy['Biomass']} MWh\n" + \
            f"💧 {energy['Hydro Run-of-river and poundage']} MWh\n" + \
            "obnovitelné ⚡ během uplynulé hodiny"
    api.update_status(status=tweet)
