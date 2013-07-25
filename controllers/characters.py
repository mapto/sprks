__author__ = 'Zhanelya'
import json
import web
from models.company import company


class characters:
    """
    Listens to ajax call which updates characters' state
    """
    def GET(self):

        #function needs to take date as an argument from ajax call and return a pair location-device for each of the 3 employees
        location_distribution = company().get_location_distribution()
        print location_distribution
        locations = json.dumps(
            {
                'interview1': 'office',
                'interview2': 'public',
                'interview3': 'home',
            }
        )
        return locations