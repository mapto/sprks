__author__ = 'Zhanelya'
import json
import web
from libraries.utils import date_utils
from models.company import company


class characters:
    """
    Listens to ajax call which updates characters' state
    """
    def POST(self):
        #takes date as an argument from ajax call and returns
        #(TODO) corresponding to this moment of time
        # pair location-device for each of the 3 employees
        #considering the distributions from company.py

        payload = json.loads(web.data())
        client_date = date_utils.iso8601_to_date(payload.get('date', '2014-01-06'))

        location_distribution = company().get_location_distribution()

        locations_devices = json.dumps(
            {
                'interviewee1': ['office','phone'],
                'interviewee2': ['public','laptop'],
                'interviewee3': ['home','desktop']
            }
        )
        return locations_devices