__author__ = 'mruskov'

from sklearn import svm
import cPickle
import numpy
import glob
import csv
import json
from models.company import company
from models.policies import policies_model as policy_model
from sim.classifier_sklearn import model_sklearn
from models.incident import incident
from models.simulation import simulation as sim_model


class train_sklearn:
    def train(self):
        """This is the main method creating the implicit model, based on the provided incidents
           It takes the incidents in static/incidents/*,json as input
           and generates static/data/classifier-models.pkl as output.
           This model is a serialization of the trained/fitted model
           Currently the CSV training set in static/data/train-generated*.csv is a by-product, but is not really needed
        """
        self.generate_training_set("classifier")
        self.generate_models("classifier")

        self.generate_training_set("regression")
        self.generate_models("regression")
        # database does not need to be generated beforehand.
        # The simulation generates it dynamically (lazy initialization)
        # self.generate_db()

    # OBSOLETE: Currently the database is filled runtime (lazy initialization)
    def generate_db(self):
        ordered_context = sim_model.ordered_context
        ordered_policy = sim_model.ordered_policy
        classifier = classifier_sklearn()
        with open('config/risks-test.sql', 'w') as f:
            f.write("DELETE FROM `risks` WHERE 1")
            for risk in classifier_sklearn.risks_set:
                for context in self.enum_policy_contexts():
                    for policy in self.enum_samples():
                        all = classifier_sklearn().predict_data(policy, self.single2plural(context))
                        cls = incident.get_most_probable(all)
                        f.write("INSERT INTO `risks` "
                            # "(`risk_type`, `employee`, `location`, `device`, `bdata`, `pdata`, `plen`, `psets`, `pdict`, `phist`, `prenew`, `pattempts`, `precovery`, `cls`, `risk_prob`) "
                            "VALUES "
                            "('" + risk)
                        for next in ordered_context:
                            f.write(", '" + context[next] + "'")
                        for next in ordered_policy:
                            f.write(", '" + str(policy[next]) + "'")
                        f.write(", " + str(cls['id']) + "', '" + str(cls['risk']) + "');\n")
                print '.'

    def single2plural(self, context):
        """ Weird, but here only one of the 27 contexts is considered,
            In the simulation you could have a group of context being represented by the same policy
        """
        result = {
            'employees': [context['employee']],
            'locations':[context['location']],
            'devices': [context['device']]}
        return result

    def enum_policy_contexts(self, partial_context = {}, start_index = 0):
        """
        Generates all possible ways to complete a partial policy.
        This is a recursive method meant to be used internally only.
        For the public use of this call generate_training_set
        :partial_policy: The policy that is currently in the process of construction
        :start_index: Used to manage progress to avoid repetitions
        """
        list = [] # policies
        ranges = {
            "employee": company.employee_types,
            "location": company.location_types,
            "device": company.device_types}
        indexedOptions = ranges.keys()

        for i in range(start_index, len(indexedOptions)): # search for first
            current = indexedOptions[i]

        # for policy in indexedOptions:
            if not current in partial_context:
                for value in ranges[current]:
                    new_partial = partial_context.copy()
                    new_partial[current] = value
                    complete_new = self.enum_policy_contexts(new_partial, start_index=i)
                    list.extend(complete_new)

                return list # stop loop when first value is found and recursion for it is done

        return [partial_context]

    def generate_models(self, type = "classifier"):
        """ Train the SVM models from the CSV dataset

        """
        print("Generating " + type + " models...")

        f = open('static/data/' + type + '-models.txt', 'wb')

        models = {}

        for risk in model_sklearn.risks_set:
            if not risk in models.keys():
                models[risk] = {}
            for employee in company.employee_types:
                if not employee in models[risk].keys():
                    models[risk][employee] = {}
                for location in company.location_types:
                    if not location in models[risk][employee].keys():
                        models[risk][employee][location] = {}
                    for device in company.device_types:
                        if not device in models[risk][employee][location].keys():
                            models[risk][employee][location][device] = {}
                        models[risk][employee][location][device] =\
                            self.train_engine(risk, employee, location, device, type=type)

        cPickle.dump(models, f)
        f.close()
        print "Model generation for " + type + " completed..."


    def generate_training_set(self, type = "classifier"):
        """
        Generalizes the incidents into a training set to be used by the implicit model.
        This assumes the types of risks
        """

        # this is iteration of incidents, values are specified in data
        print "Generating " + type + " training set..."
        entries = {}
        eng = engine.get_engine(type=type)

        # read incidents and generate training sets
        for ref in glob.glob('static/incidents/*.json'):
            file = open(ref)
            incident = json.load(file)
            file.close()

            risk = incident["type"]
            policy = incident["policy"]
            cls = incident["id"]
            value = incident["risk"]

            print str(incident["name"]) + " " + str(cls) + " type: " + str(risk) + " value: " + str(value)

            # for a policy that has undefined values this returns all possible combinations
            samples = self.enum_samples(policy)

            # add classification last column
            for sample in samples:
                data = policy_model.policy2datapoint(sample)
                data.append(incident[eng.get_result_field()]) # add last column with classification for printing in CSV

                if risk not in entries:
                    entries[risk] = []
                entries[risk].append(data)  # put them in a risk dictionary

        for risk in entries.keys():
            for employee in company.employee_types:
                for location in company.location_types:
                    for device in company.device_types:
                        self.dump_training_set(entries, risk, employee, location, device, type=type)

        print "Training set generation for " + type + " completed..."

    def dump_training_set(self, entries, risk, employee, location, device, type="classifier"):
        #save the risk dictionary files
        context = employee + '-' + location + '-' + device
        tail = 'general' if risk == 'general' else risk + '-' + context

        csv_name = 'static/data/train-' + type + '-' + tail + '.csv'
        print csv_name
        writer = csv.writer(open(csv_name, 'w'))
        for row in entries[risk]:
            print row
            writer.writerow(row)

    def enum_samples(self, partial_policy = {}, start_index = 0):
        """
        Generates all possible ways to complete a partial policy.
        This is a recursive method meant to be used internally only.
        For the public use of this call generate_training_set
        :partial_policy: The policy that is currently in the process of construction
        :start_index: Used to manage progress to avoid repetitions
        """
        list = [] # policies
        indexedOptions = policy_model.get_ranges().keys()

        for i in range(start_index, len(indexedOptions)): # search for first
            policy = indexedOptions[i]

        # for policy in indexedOptions:
            if not policy in partial_policy:
                for value in policy_model.get_ranges()[policy]:
                    new_partial = partial_policy.copy()
                    new_partial[policy] = value
                    complete_new = self.enum_samples(new_partial, start_index=i)
                    list.extend(complete_new)

                return list # stop loop when first value is found and recursion for it is done

        return [partial_policy]

    def load_csv_files(self, risk, employee, location, device, type="classifier"):
        context = employee+'-'+location+'-'+device
        general = numpy.genfromtxt('static/data/train-' + type + '-general.csv', delimiter=',')
        filenames = glob.glob('static/data/train-' + type + '-'+risk+'-'+ context +'.csv')

        data = numpy.genfromtxt(filenames[0], delimiter=',')
        data = numpy.concatenate((data, general)) # add positive cases that need to contrast negative ones

        return data

    def train_engine(self, risk, employee, location, device, type="classifier"):
        data = self.load_csv_files(risk, employee, location, device, type=type)
        limit = len(policy_model.get_ranges())

        train_data = data[:, 0:limit] # first several columns represent the data dimension
        train_result = data[:, limit] # result columns are ones after data dimensions

        # for explanation of the following parameters please see
        # http://scikit-learn.org/stable/modules/svm.html#tips-on-practical-use
        params = {'kernel': 'rbf', 'cache_size': 1000, 'C': 0.9}
        eng = engine.get_engine(type=type)
        return eng.get_model(params).fit(train_data, train_result)

class engine:
    def __init__(self):
        pass

    @staticmethod
    def get_engine(type="classifier"):
        if type == "regression":
            result = regression_engine()
        else:
            result = classifier_engine()
        return result

    def get_model(self, params):
        raise NotImplementedError

    def get_result_field(self):
        raise NotImplementedError

class classifier_engine(engine):
    def __init__(self):
        self.type = "classifier"
        engine.__init__(self)

    def get_model(self, params):
        return svm.SVC(**params)

    def get_result_field(self):
        return 'id'

class regression_engine(engine):
    def __init__(self):
        self.type = "regression"
        engine.__init__(self)

    def get_model(self, params):
        return svm.SVR(**params)

    def get_result_field(self):
        return 'risk'

if __name__ == "__main__":
    # train_sklearn().train()
    """
    result = train_sklearn().enum_samples({})
    for next in result:
        print policy_model.policy2datapoint(next)

    print len(result)

    print len(train_sklearn().enum_policy_contexts())
    """
    """
    product = 1
    for next in policy_model.get_ranges():
        product = product * len(policy_model.get_ranges()[next])
        print next
        print policy_model.get_ranges()[next]
        print len(policy_model.get_ranges()[next])
    print product
    """
    # print train_sklearn().enum_policy_contexts()
    # train_sklearn().generate_db()
    train_sklearn().train()
