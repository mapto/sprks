__author__ = 'zcabh_000'

import glob
import json
from models.pw_policy import pw_policy_model

class incident:
    # names = ['default', 'too_often', 'very_easy', 'eternal', 'too_hard', 'easy_recovery', 'infrequent_use', 'easy_secure', 'hard_secure', 'no_pass']
    incidents = {} # will contain {"bruteforce": []}"
    singleton = None

    @staticmethod
    def read_files():
        for ref in glob.glob('static/incidents/*.json'):
            file = open(ref)
            data = json.load(file)

            risk_type = data["type"]
            if not risk_type in incident.incidents:
                incident.incidents[risk_type] = {}

            incident.incidents[risk_type][data["id"]] = data

            file.close()
            # print data["name"] + " " + str(data["id"])


    @staticmethod
    def get_incident(id='1', type='any'): # if type not specified, search
        if not incident.incidents:
            incident.read_files()


        if type == "any": # search and return the first one found
            for risk in incident.incidents.keys():
                if id in incident.incidents[risk]:
                    # print "found: " + "[" + str(id) + "] in class " + risk + " ->" + str(incident.incidents[risk][id]['name']) +  " " + str(incident.incidents[risk][id]['risk'])

                    return incident.incidents[risk][id]
        else:
            return incident.incidents[type][id]

    def generate_samples(self):
        list = []
        for policy in pw_policy_model.range.keys():
            if not policy in self.data['pwpolicy']:
                list.push()

    # the following list of getters and setters might be incomplete
    def get_description(self):
        return self.data['description']

    def get_name(self):
        return self.data['name']

    def get_consequences(self):
        return self.data['consequences']

    def get_event(self):
        return self.data['event']

    def get_type(self):
        return self.data['type']

    def get_id(self):
        return self.data['id']

    def get_cost(self):
        return self.data['cost']

    def get_risk(self):
        return self.data['risk']
