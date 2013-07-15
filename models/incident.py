import glob
import json
from models.pw_policy import pw_policy_model


class incident:
    """ To generate the incidents dataset call generate_policy_dataset in pwpolicy_model
    """
    # names = ['default', 'too_often', 'very_easy', 'eternal', 'too_hard', 'easy_recovery', 'infrequent_use', 'easy_secure', 'hard_secure', 'no_pass']
    incidents = {} # will contain {"bruteforce": []}"
    singleton = None

    @classmethod
    def read_files(self):
        for ref in glob.glob('static/incidents/*.json'):
            f = open(ref)
            data = json.load(f)

            risk_type = data["type"]
            if not risk_type in incident.incidents:
                incident.incidents[risk_type] = {}

            incident.incidents[risk_type][data["id"]] = data
            f.close()
            # print data["name"] + " " + str(data["id"])


    @classmethod
    def get_incident(self, ident='1', typ='any'): # if type not specified, search
        """
        Factory method (http://en.wikipedia.org/wiki/Factory_method_pattern) for incidents
        :ident: The incident id. This must be present in the static/incidents files
        :typ: if you know the risk that this incident is associated, specify it here. Otherwise it will search all of them
        """
        if not incident.incidents:
            incident.read_files()

        if typ == "any": # search and return the first one found
            for risk in incident.incidents.keys():
                if ident in incident.incidents[risk]:
                    # print "found: " + "[" + str(id) + "] in class " + risk + " ->" + str(incident.incidents[risk][id]['name']) +  " " + str(incident.incidents[risk][id]['risk'])

                    return incident.incidents[risk][ident]
        else:
            return incident.incidents[typ][ident]

    @classmethod
    def get_incident_by_name(self, name='infrequent_use'): # if type not specified, search
        ref = 'static/incidents/' + name + '.json'
        f = open(ref)
        data = json.load(f)
        f.close()

        ident = data["id"]
        typ = data["type"]

        return incident.incidents[typ][ident]

    def generate_samples(self):
        l = []
        for policy in pw_policy_model.ranges.keys():
            if not policy in self.data['pwpolicy']:
                l.push()

    # the following list of getters and setters might be incomplete
    def get_description(self):
        return self.data['description']

    def get_consequences(self):
        return self.data['consequences']

    def get_event(self):
        return self.data['event']

    def get_name(self):
        return self.data['name']

    def get_type(self):
        return self.data['type']

    def get_id(self):
        return self.data['id']

    def get_cost(self):
        return self.data['cost']

    def get_risk(self):
        return self.data['risk']
