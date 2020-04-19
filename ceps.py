import xml.etree.ElementTree as ET
import requests
import datetime

def prepare_params(energy_type, **kwargs):
    params = kwargs
    today = datetime.date.today().isoformat()
    this_hour = datetime.datetime.now().hour
    params['dateFrom'] = f'{today} {this_hour-1}:00:00'
    params['dateTo'] = f'{today} {this_hour}:00:00'
    params['para1'] = energy_type
    return params

def get_energy_for_now(url, params): 
    r = requests.post(url, params)
    root = ET.fromstring(r.content)
    value_key = root[1][0].attrib['id']
    energy = {'date': root[2][0].attrib['date'],\
            'value': root[2][0].attrib[value_key],\
            'energy_type': params['para1']}
    return energy

def get_for_all(url, energy_types):
    energy_all = []
    for kind in energy_types:
        params = prepare_params(kind, agregation='HR', function='AVG', version='RT')
        energy_all.append(get_energy_for_now(url, params))
    return energy_all

if __name__ == '__main__':
    ceps_url = 'https://wwwtest.ceps.cz//_layouts/CepsData.asmx/Generation'
    energy_types = ['PE', 'PPE', 'JE', 'VE', 'PVE', 'AE', 'ZE', 'FVE', 'VTE']
    energy_types_dict = {
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
    all_energy = get_for_all(ceps_url, energy_types)
    print(all_energy)
