import glob
import json


class incident:
    """ To generate the incidents dataset call generate_policy_dataset in pwpolicy_model
    """
    # names = ['default', 'too_often', 'very_easy', 'eternal', 'too_hard', 'easy_recovery', 'infrequent_use', 'easy_secure', 'hard_secure', 'no_pass']
    incidents = {} # will contain {"bruteforce": []}"
    singleton = None

    def __init__(self):
        self.read_files()

    @classmethod
    def read_files(cls):
        for ref in glob.glob('static/incidents/*.json'):
            f = open(ref)
            data = json.load(f)

            risk_type = data["type"]
            if not risk_type in incident.incidents:
                incident.incidents[risk_type] = {}

            incident.incidents[risk_type][data["id"]] = data
            print "files read"
            f.close()
            # print data["name"] + " " + str(data["id"])

    @classmethod
    def get_incident(cls, ident='1', typ='any'): # if type not specified, search
        """
        Factory method (http://en.wikipedia.org/wiki/Factory_method_pattern) for incidents
        :param ident: The incident id. This must be present in the static/incidents files
        :param typ: if risk that this incident is associated is known, specify it. Otherwise it will search all of them
        """
        if not incident.incidents:
            print "reading files"
            incident.read_files()
        print "finished testing"
        if typ == "any": # search and return the first one found
            print "type is any"
            print incident.incidents
            for risk in incident.incidents.keys():
                print "getting risk"
                try:
                    print "getting incidents"
                    print incident.incidents[risk]
                    print "ident"
                    print ident
                    inc = incident.incidents[risk].get(ident)
                    if inc != None:
                        return incident.incidents[risk].get(ident)
                except KeyError:
                    print incident.incidents[risk]
                    print 'fail, ident=' + str(ident)
                # if ident in incident.incidents[risk]:

                    # print "found: " + "[" + str(id) + "] in class " + risk + " ->" + str(incident.incidents[risk][id]['name']) +  " " + str(incident.incidents[risk][id]['risk'])


        else:
            return incident.incidents[typ][ident]

    #OBSOLETE
    @classmethod
    def get_incident_by_name(cls, name='infrequent_use'): # if type not specified, search
        ref = 'static/incidents/' + name + '.json'
        f = open(ref)
        data = json.load(f)
        f.close()

        ident = data["id"]
        typ = data["type"]

        return incident.incidents[typ][ident]

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

if __name__ == "__main__":
    #incident.read_files()
    print incident.get_incident(5)
