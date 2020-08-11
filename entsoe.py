import requests
import xmltodict

def get_renewable_energy(url, params, res_map):
    """Get energy data based on params.
    Returns dictionary with energy from renewable sources.
    """
    energy = {}
    r = requests.get(url, params=params)
    if r.status_code != 200:
        return None
    d = xmltodict.parse(r.text)
    for serie in d['GL_MarketDocument']['TimeSeries']:
        psr_type = serie['MktPSRType']['psrType']
        quantity = serie['Period']['Point']['quantity']
        if psr_type in res_map:
            energy[res_map[psr_type]] = quantity
    return energy

url = 'https://transparency.entsoe.eu/api?'

params = {
    'securityToken': None,
    'In_Domain': '10YCZ-CEPS-----N',
    'ProcessType': 'A16',
    'DocumentType': 'A75',
    'TimeInterval': None,
    }

res_map = {
    'B01': 'Biomass',
    'B11': 'Hydro Run-of-river and poundage',
    'B15': 'Other renewable',
    'B16': 'Solar',
    'B19': 'Wind Onshore',
    }
