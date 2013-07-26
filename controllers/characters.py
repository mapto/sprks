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
        
        locations = json.dumps(
            {
                'interviewee1': ['office','phone'],
                'interviewee2': ['public','laptop'],
                'interviewee3': ['home','desktop']
            }
        )
        return locations