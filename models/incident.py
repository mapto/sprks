import glob
import json


class incident:
    """ To generate the incidents dataset call generate_policy_dataset in pwpolicy_model
    """
    # names = ['default', 'too_often', 'very_easy', 'eternal', 'too_hard', 'easy_recovery', 'infrequent_use', 'easy_secure', 'hard_secure', 'no_pass']
    incidents = {} # will contain {"bruteforce": []}"
    singleton = None

    @classmethod
    def get_most_probable(cls, incidents):
        """ Compares all incidents in the list and returns the most probable one.
            Please make sure to have objects, not only ids when making the call
            :param incidents: a list of incident objects
        """
        max = incidents[0]
        for next in incidents:
            if max['risk'] < next['risk']:
                max = next
        return max

    @classmethod
    def read_files(cls):
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
    def get_incident(cls, ident='1', typ='any'): # if type not specified, search
        """
        Factory method (http://en.wikipedia.org/wiki/Factory_method_pattern) for incidents
        Used by both sim and incident controller. type(ident) may be either 'int', 'unicode', or 'string'.
        If type not specified, search all.

        :param ident: The incident id. This must be present in the static/incidents files
        :param typ: if risk that this incident is associated is known, specify it. Otherwise it will search all of them
        """

        if not incident.incidents:
            incident.read_files()

        if typ == "any": # search and return the first one found
            for risk in incident.incidents.keys():

                try:
                    # print incident.incidents[risk][int(ident)]
                    # print 'returning'
                    return incident.incidents[risk][int(ident)]
                except KeyError:
                    # print incident.incidents[risk]
                    print 'fail, ident=' + str(ident) + ' risk=' + risk
                except ValueError:
                    return 'Identifier should be a number'
                # if ident in incident.incidents[risk]:

                    # print "found: " + "[" + str(id) + "] in class " + risk + " ->" + str(incident.incidents[risk][id]['name']) +  " " + str(incident.incidents[risk][id]['risk'])

                print 'Not found'

        else:
            return incident.incidents[typ][ident]

    #OBSOLETE
    @classmethod
    def get_incident_by_name(self, name='default'): # if type not specified, search
        ref = 'static/incidents/' + name + '.json'
        f = open(ref)
        data = json.load(f)
        f.close()

        ident = data["id"]
        typ = data["type"]

        if not incident.incidents:
            incident.read_files()

        return incident.incidents[str(typ)][ident]

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
