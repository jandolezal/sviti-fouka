
import xml.etree.ElementTree as ET
import datetime
import xmltodict
import requests
from credentials import token

def add_past_hour_to_params(params):
    """Add PeriodStart and  PeriodEnd to params.
    """
    now = datetime.datetime.utcnow()
    year = now.year
    month = str(now.month).zfill(2)
    day = str(now.day).zfill(2)
    last_hour = str(now.hour-1).zfill(2)
    hour = str(now.hour).zfill(2)
    params['PeriodStart'] = f'{year}{month}{day}{last_hour}00'
    params['PeriodEnd'] = f'{year}{month}{day}{hour}00'
    return params

def add_source_to_params(res_type, params):
    """Add PsrType (power source type) to params.
    """
    params['PsrType'] = res_type
    return params

def get_energy(url, params):
    """Get energy data based on params.
    Returns string with a value in MWh.
    """
    r = requests.get(url, params=params)
    root = ET.fromstring(r.text)
    energy = root[10][7][2][1].text
    return energy

def get_past_hour_energy(res, default_params):
    """Get energy generation from resource (res) in last hour.
    Returns string with a value in MWh.
    """
    params = add_past_hour_to_params(default_params)
    params = add_source_to_params(res_type[res], params)
    biomass = get_energy(production_url, params)
    return biomass

res_type = {'Biomass': 'B01', 'Hydro Run-of-river and poundage': 'B11',\
            'Other renewable': 'B15', 'Solar': 'B16', 'Wind Onshore': 'B19'}

production_url = 'https://transparency.entsoe.eu/api?'

default_params = {'securityToken': token, 'In_Domain': '10YCZ-CEPS-----N',\
    'ProcessType': 'A16', 'DocumentType': 'A75','PeriodStart': '', 'PeriodEnd': ''}
