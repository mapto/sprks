from libraries import db_helper
from localsys.storage import db
import csv
import glob
import json
from localsys.storage import db

class pw_policy_model:

    ranges = {"plen": [0, 6, 8, 10, 12],
              "psets": [1, 2, 3, 4],
              "pdict": [0, 1],
              "phist": [1, 2, 3, 4],
              "prenew": [0, 1, 2, 3],
              "pattempts": [0, 1, 2],
              "precovery": [0, 1, 2]}

    @staticmethod
    def policy2datapoint(policy):
        if type(policy["plen"]) == int:
            return [policy["plen"], policy["psets"],
                    policy["pdict"], policy["phist"],
                    policy["prenew"], policy["pattempts"],
                    policy["precovery"]]
        else:
            return [policy["plen"], policy["psets"],
                    policy["pdict"], policy["phist"],
                    policy["prenew"], policy["pattempts"],
                    policy["precovery"]]

    @classmethod
    def update(cls, where, values):
        """
        Generates query string using db_helper.update_helper.stringify, and runs db.query.
        """
        return db.query(db_helper.update_helper.stringify('pw_policy', where, values), vars=locals())

    @classmethod
    def latest_policy(self, user_id):
        policy = {
            'location': "",
            'employee': "",
            'device': "",
            'bdata': "",
            'pdata': "",
            'plen': 8,
            'psets': 2,
            'pdict': 0,
            'phist': 1,
            'prenew': 1,
            'pattempts': 0,
            'precovery': 1,
        }
        db_policy_all = db.select('policies', where="user_id=$user_id", order="date DESC", vars=locals())
        if len(db_policy_all):
            db_policy = db_policy_all[0]
            db_bio = db.select('biometrics', where="id=$db_policy.bio_id", vars=locals())[0]
            db_pass = db.select('passfaces', where="id=$db_policy.pass_id", vars=locals())[0]
            db_pw = db.select('pw_policy_test', where="id=$db_policy.pw_id", vars=locals())[0]
            policy["location"] = db_policy.location
            policy["employee"] = db_policy.employee
            policy["device"] = db_policy.device
            policy["bdata"] = db_bio.bdata
            policy["pdata"] = db_pass.pdata
            policy["plen"] = db_pw.plen
            policy["psets"] = db_pw.psets
            policy["pdict"] = db_pw.pdict
            policy["phist"] = db_pw.phist
            policy["prenew"] = db_pw.prenew
            policy["pattempts"] = db_pw.pattempts
            policy["precovery"] = db_pw.precovery

        return policy

    def generate_samples(self, partial_policy, start_index = 0):
        """ Generates all possible ways to complete a partial policy
        """
        list = [] # policies
        indexedOptions = self.ranges.keys()
        # complete = (start_index + 1 == len(indexedOptions)) # returns bool

        for i in range(start_index, len(indexedOptions)): # search for first
            policy = indexedOptions[i]

        # for policy in indexedOptions:
            if not policy in partial_policy:
                for value in self.ranges[policy]:
                    new_partial = partial_policy.copy()
                    new_partial[policy] = value
                    complete_new = self.generate_samples(new_partial, start_index=i)
                    list.extend(complete_new)

                return list # stop loop when first value is found and recursion for it is done

        return [partial_policy]

    def generate_training_set(self):
        entries = {"bruteforce": [], "stolen": [], "general": [] }

        # read incidents and generate training sets
        for ref in glob.glob('static/incidents/*.json'):
            file = open(ref)
            incident = json.load(file)
            file.close()

            risk = incident["type"]
            policy = incident["pwpolicy"]
            cls = incident["id"]

            print str(incident["name"]) + " " + str(cls) + " type: " + str(risk)

            # for a policy that has undefined values this returns all possible combinations
            samples = self.generate_samples(policy)

            # add classification last column
            for sample in samples:
                data = self.policy2datapoint(sample)
                data.append(cls) # add last column with classification for printing in CSV
                entries[risk].append(data)  # put them in a risk dictionary

        #save the risk dictionary files
        for risk in entries.keys():
            tail = 'general' if risk == 'general' else 'risk-' + risk

            csv_name = 'static/data/pw-train-generated-' + tail + '.csv'
            print csv_name
            writer = csv.writer(open(csv_name, 'w'))
            for row in entries[risk]:
                print row
                writer.writerow(row)

    def create_variation(self, policy, id, value):
        new_policy = {}
        for key in policy:
            new_policy[key] = policy[key]
        new_policy[id] = value
        return new_policy

    def get_range(self, policy, id):
        msgs = []
        sets = self.ranges
        for value in sets[id]:
            new_policy = self.create_variation(policy, id, value)
            msg = {}
            msg['id'] = id+str(value)
            msg["data"] = new_policy
            msgs.append(msg)
        return msgs

    def parse_policy(self, policyUpdate):
        policies = {}
        for update in policyUpdate:
            for empl in update['employee']:
                for loc in update['location']:
                    for dev in update['device']:
                        for key, value in update['policyDelta'].iteritems():



if __name__ == "__main__":
    model = pw_policy_model()
    # result = model.generate_samples({'prenew': 3, 'pattempts': 3, 'pdict': 0, 'psets': 2, 'phist': 4})
    # result = model.generate_samples({'plen': 0})
    # result = model.generate_samples({})
    #model.generate_training_set()
    policy = model.latest_policy(3)
    print policy

