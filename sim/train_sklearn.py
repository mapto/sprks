__author__ = 'mruskov'

from sklearn import svm
from sklearn import __version__ as sklearn_ver
import cPickle
import numpy
import glob
import csv
import json
import os
from localsys import storage
from models.company import company
from models.policies import policies_model as policy_model
from sim.model_sklearn import model_sklearn


class train_sklearn:
    types = ["classifier", "regression"]

    def update(self):
        for next in self.types:
            if not os.path.exists('static/data/' + next  + '-models-' + sklearn_ver + '.pkl'):
                self.train(next)

    def train(self):
        """This is the main method creating the implicit model, based on the provided incidents
           It takes the incidents in static/incidents/*,json as input
           and generates static/data/*-models-*.pkl as output.
           This model is a serialization of the trained/fitted model
           Currently the CSV training set in static/data/train-generated*.csv is a by-product, but is not really needed
        """
        for type in self.types:
            self.generate_training_set(type)
            self.generate_models(type)

        # database does not need to be generated beforehand.
        # The simulation generates it dynamically (lazy initialization)
        # Still previous database should better be dropped to avoid inconsistencies
        self.clean()

    def clean(self):
        self.clean_db()
        self.clean_files()

    def clean_files(self):
        for ref in glob.glob('static/data/train-*.csv'):
            os.remove(ref)

    def clean_db(self):
        storage.db.query("DELETE FROM `risks` WHERE 1")

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

        f = open('static/data/' + type + '-models-' + sklearn_ver + '.pkl', 'wb')

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
        params = {'kernel': 'rbf', 'cache_size': 1000, 'C': 0.2, 'gamma': 0.5}
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
    #train_sklearn().cleanup()
