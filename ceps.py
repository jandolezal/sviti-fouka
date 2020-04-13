import xml.etree.ElementTree as ET
import requests
import datetime

CEPS_GENERATION = 'https://wwwtest.ceps.cz//_layouts/CepsData.asmx/Generation'
DATA = {
    'agregation': 'HR',
    'function': 'AVG',
    'version': 'RT',
    }
ENERGY_TYPES = ['PE', 'PPE', 'JE', 'VE', 'PVE', 'AE', 'ZE', 'FVE', 'VTE']
ENERGY_TYPES_DICT = {
    'PE': 'parní',
    'PPE' : 'plynové a paroplynové',
    'JE': 'jaderné',
    'VE': 'vodní',
    'PVE': 'přečerpávací vodní',
    'AE': 'alternativní',
    'ZE': 'závodní',
    'FVE': 'fotovoltaické',
    'VTE': 'větrné'
    }

def get_energy_for_now(energy_type, agregation='HR', function='AVG', version='RT'):
    data = DATA
    today = datetime.date.today().isoformat()
    this_hour = datetime.datetime.now().hour
    data['dateFrom'] = f'{today} {this_hour-1}:00:00'
    data['dateTo'] = f'{today} {this_hour}:00:00'
    data['para1'] = energy_type
    r = requests.post(CEPS_GENERATION, data)
    root = ET.fromstring(r.content)
    value_key = root[1][0].attrib['id']
    energy = {'date': root[2][0].attrib['date'], 'value': root[2][0].attrib[value_key], 'energy_type': energy_type}
    return energy

def get_for_all(energy_types):
    energy_all = []
    for kind in energy_types:
        energy_all.append(get_energy_for_now(kind))
    return energy_all

if __name__ == '__main__':
    all_energy = get_for_all(ENERGY_TYPES)
    print(all_energy)
