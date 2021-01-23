import requests
import xml.etree.ElementTree as ET


def request_data(url, params):
    r = requests.get(url, params=params)
    if r.status_code != 200:
        return None
    return r.text


def parse_xml(xml, res_map):
    """Parses renewable energy from xml string.
    """
    energy = {}
    root = ET.fromstring(xml)
    ns = '{urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0}'
    for serie in root.iter(ns + 'TimeSeries'):
        psr_type = serie.find(ns + 'MktPSRType').find(ns + 'psrType').text
        quantity = serie.find(ns + 'Period').find(ns + 'Point').find(ns + 'quantity').text
        if psr_type in res_map:
            energy[res_map[psr_type]] = quantity
    return energy


def data_check(energy):
    for entry in energy.values():
        try:
            int(entry)
        except (TypeError, ValueError):
            return False
    return True


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
