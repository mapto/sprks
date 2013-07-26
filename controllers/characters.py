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

        #function needs to take date as an argument from ajax call and return a pair location-device for each of the 3 employees
        payload = json.loads(web.data())

        client_date = date_utils.iso8601_to_date(payload.get('date', '2014-01-06'))
        print client_date
        location_distribution = company().get_location_distribution()

        locations_devices = json.dumps(
            {
                'interviewee1': ['office','phone'],
                'interviewee2': ['public','laptop'],
                'interviewee3': ['home','desktop']
            }
        )
        return locations_devices