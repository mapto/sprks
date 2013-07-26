__author__ = 'Zhanelya'
import json
import web
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
        client_date = date_utils.iso8601_to_date(payload.get('date'))
        start_date = date_utils.iso8601_to_date('2014-01-06')

        days_delta = (client_date - start_date).days

        locations, devices = self.get_locations_devices(days_delta)

        locations_devices = json.dumps(
            {
                'interviewee1': [locations[0],devices[0]],  # Susie (executive)
                'interviewee2': [locations[1],devices[1]],  # Kevin (desk)
                'interviewee3': [locations[2],devices[2]]   # Iza (road)
            }
        )
        return locations_devices

    def get_locations_devices(self, days_delta):
        """
        Function deriving locations and devices array
        from the csv files considering timedelta(current_client_time - start_time)
        #1 day is taken as a time unit -> 100days corresponds to 100%
        """

        mod = (days_delta % 100)/float(100)
        print days_delta
        print mod
        locations = [None] * 3
        devices = [None] * 3

        #locations for interviewees(1,2,3)
        employees2locations = company().employees2locations
        for i in range(0, 3):
            if mod <= employees2locations[0, :][i]:    # percentage derived from locations.csv
                locations[i] = 'home'
            else:
                if mod <= (employees2locations[0, :][i])+(employees2locations[1, :][i]):    # (percentage from locations.csv) + (previous one)
                    locations[i] = 'public'
                else:
                    if mod > (employees2locations[0, :][i])+(employees2locations[1, :][i]):
                        locations[i] = 'office'

        #devices for interviewees(1,2,3)
        employees2devices = company().employees2devices
        for i in range(0, 3):
            if mod <= employees2devices[0, :][i]:    # percentage derived from devices.csv
                devices[i] = 'desktop'
            else:
                if mod <= (employees2devices[0, :][i])+(employees2devices[1, :][i]):    # (percentage from devices.csv) + (previous one)
                    devices[i] = 'laptop'
                else:
                    if mod > (employees2devices[0, :][i])+(employees2devices[1, :][i]):
                        devices[i] = 'phone'

        return locations, devices