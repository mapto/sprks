__author__ = 'Zhanelya'
import json
import web
from datetime import date
from libraries.utils import date_utils
from models.company import company


class characters:
    """
    Types of characters:
    employee_types = {'executives', 'desk', 'road'}

    Listens to ajax call which updates characters' state:
    location_types = {'office', 'public', 'home'}
    device_types = {'desktop', 'laptop', 'phone'}
    """
    def POST(self):
        #takes date as an argument from ajax call and returns
        #corresponding to this moment of time
        # pair location-device for each of the 3 employees
        #considering the distributions from company.py

        payload = json.loads(web.data())
        client_date = date_utils.iso8601_to_date(payload.get('date', '2014-01-06'))
        start_date = date_utils.iso8601_to_date('2014-01-06')

        days_delta = (client_date - start_date).days

        locations, devices = self.get_locations_devices(days_delta)

        locations_devices = json.dumps(
            {
                'interviewee1': [locations[0],devices[0]],
                'interviewee2': [locations[1],devices[1]],
                'interviewee3': [locations[2],devices[2]]
            }
        )
        return locations_devices

    def get_locations_devices(self, days_delta):
        #TODO function deriving locations and devices array from the timedelta(current_client_time - start_time)
        locations = []
        devices = []
        if (days_delta % 10) <= 1:                      # mod <= 1
            locations = ['home', 'home', 'home']         # location [interviewee1, interviewee2, interviewee3]
            devices = ['laptop', 'laptop', 'laptop']     # device [interviewee1, interviewee2, interviewee3]
        else:
            if (days_delta % 10) <= 6:                  # 1 < mod <= 6
                locations = ['office', 'office', 'office']
                devices = ['desktop', 'desktop', 'desktop']
            else:                                       # mod > 6
                locations = ['public', 'public', 'public']
                devices = ['phone', 'phone', 'phone']

        #may be used later for getting the appropriate time distribution (now being hardcoded):
        #location_distribution = company().get_location_distribution()

        return locations, devices