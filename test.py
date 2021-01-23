import unittest
import os

from dotenv import load_dotenv

from entsoe import url, params, res_map, request_data, parse_xml


timeinterval = '2021-01-23T12%2F2021-01-23T13'

data = {
    'Biomass': '312',
    'Hydro Run-of-river and poundage': '129',
    'Other renewable': '284',
    'Solar': '186',
    'Wind Onshore': '138',
    }

load_dotenv()


class EntsoeParserTest(unittest.TestCase):

    def test_2021_01_23_13_hours(self):
        # Update params to make a Entsoe API request
        params['securityToken'] = os.getenv('ENTSOE_TOKEN')
        params['TimeInterval'] = timeinterval

        # Get energy for past hour from Entsoe API
        test_data = request_data(url, params)
        energy = parse_xml(test_data, res_map)

        self.assertDictEqual(energy, data)
