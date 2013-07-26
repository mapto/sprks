__author__ = 'Zhanelya'
import json
import web
from datetime import date
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
        start_date = date_utils.iso8601_to_date('2014-01-06')

        days_delta = (client_date - start_date).days
        location = []

        if (days_delta % 10) <= 1:                      # mod <= 1
            location = ['home', 'home', 'home']         # location [interviewee1, interviewee2, interviewee3]
        else:
            if (days_delta % 10) <= 6:                  # 1 < mod <= 6
                location = ['office', 'office', 'office']
            else:                                       # mod > 6
                location = ['public', 'public', 'public']

        #may be used later for getting the appropriate time distribution (now being hardcoded):
        #location_distribution = company().get_location_distribution()


        locations_devices = json.dumps(
            {
                'interviewee1': [location[0],'phone'],
                'interviewee2': [location[1],'laptop'],
                'interviewee3': [location[2],'desktop']
            }
        )
        return locations_devices