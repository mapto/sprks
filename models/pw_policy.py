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
              "pautorecover": [0, 1, 2]}

    @staticmethod
    def policy2datapoint(policy):
        if type(policy["plen"]) == int:
            return [policy["plen"], policy["psets"],
                    policy["pdict"], policy["phist"],
                    policy["prenew"], policy["pattempts"],
                    policy["pautorecover"]]
        else:
            return [policy["plen"], policy["psets"],
                    policy["pdict"], policy["phist"],
                    policy["prenew"], policy["pattempts"],
                    policy["pautorecover"]]

    def update(self, where, values):
        """
        Generates query string using db_helper.update_helper.stringify, and runs db.query.
        """
        return db.query(db_helper.update_helper.stringify('pw_policy', where, values), vars=locals())

    def latest_policy(self):
        pass

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


if __name__ == "__main__":
    model = pw_policy_model()
    # result = model.generate_samples({'prenew': 3, 'pattempts': 3, 'pdict': 0, 'psets': 2, 'phist': 4})
    # result = model.generate_samples({'plen': 0})
    # result = model.generate_samples({})
    model.generate_training_set()


