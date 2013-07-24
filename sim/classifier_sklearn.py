__author__ = 'Daniyar'

from sklearn import svm
import cPickle
import numpy
import glob
import csv
import json
from models.pw_policy import pw_policy_model as pw_policy
from models.company import company
from models.incident import incident
from models.policies import policies_model as policy_model


class classifier_sklearn:
    risks_set = ["bruteforce", "stolen"] # this needs to be derived from actual incident json files

    def __init__(self, type="classifier"):
        """
        Initializes all implicit models.
        Currently there is one model per risk,
        but should turn into one model per risk per environmental configuration


        :param type: "classifier" or "estimator"
        """
        self.incidents_models = {}
        self.risks = []
        check_classifier = True
        f = open('static/data/' + type + '-models.txt','rb')
        self.incidents_models = cPickle.load(f)
        f.close()


    def predict_data(self, data):
        """
        Makes a prediction for a particular policy
        Currently only handles pw_policy, but in future data preparation needs to be handled by the model.
        :param data: The policy configuration that needs to be consistent with the used data structure
        """
        datapoints = policy_model.policy2datapoint(data)
        result = self.predict_datapoint(datapoints)
        return result

    def predict_datapoint(self, datapoints):
        """
        Makes a prediction for a particular policy datapoint, given all implicit models
        For external use, please refer to predict_data
        :param datapoint: The data as a tuple
        """
        greatest = None

        risks_list = []
        tmp_list = {}

        #for risk in self.risks:
        """
        Iterates through classifier models to estimate class for different locations, workers and devices
        Returns list of incident IDs
        """
        for risk in classifier_sklearn.risks_set:
            my_list = []
            for employee in company.employee_types:
                for location in company.location_types:
                    for device in company.device_types:
                        models = self.incidents_models
                        model = models[risk][employee][location][device]
                        response = self.incidents_models[risk][employee][location][device].predict(datapoints)
                        cls = int(response[0]) # algorithm returns float, we need to match it to string defined in json
                        # data is returned as an array of numpy.float64, we need integers so we could use them as incident indices
                        # event = incident(cls[0].astype(int64))
                        # risk = event.get_risk()
                        event = incident.get_incident(cls)
                        my_list.append({'id': event['id'], 'risk': event['risk']})
                        #risks_list.append(event["id"])
            tmp_list[risk] = my_list
            #if greatest is None or event["risk"] > greatest[1]:
            #   greatest = [event["name"], event["risk"]] # 0 - name, 1 - risk

        """
        Finds the incident with maximum risk probability
        """
        for risk in tmp_list:
            tmp_id = tmp_list[risk][0]['id']
            max = tmp_list[risk][0]['risk']
            for tmp_incident in tmp_list[risk]:
                if tmp_incident['risk'] > max:
                    max = tmp_incident['risk']
                    tmp_id = tmp_incident['id']
            risks_list.append(tmp_id)
            #max = 1

        return risks_list
        #return self.incidents_model.predict(data)

class trainer_sklearn:
    """This is the object creating the implicit model, based on the provided incidents
       It takes the incidents in static/incidents/*,json as input
       and generates static/data/?-models.pkl as output, depending whether classification or regression is requested
       This model is a serialization of the trained/fitted model
       Currently the CSV training set in static/data/train-?-*.csv is a by-product, but is not really needed
    """
    def __init__(self):
        self.type = "classifier"
        self.generate_training_set()
        self.generate_models()
        self.type = "estimator"
        self.generate_training_set()
        self.generate_models()

    def generate_models(self):
        """ Train the SVM models from the CSV dataset

        """
        print "Generating " + self.type + " models..."

        f = open('static/data/' + self.type + '-models.txt', 'wb')

        models = {}

        for risk in classifier_sklearn.risks_set:
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
                        models[risk][employee][location][device] = self.train_classifier(risk, employee, location, device)

        cPickle.dump(models, f)
        f.close()
        print "Model generation for " + self.type + " completed..."

    def generate_training_set(self):
        """
        Generalizes the incidents into a training set to be used by the implicit model.
        This assumes the types of risks
        """

        # this is iteration of incidents, values are specified in data
        print "Generating " + self.type + " training set..."
        entries = {}

        # read incidents and generate training sets
        for ref in glob.glob('static/incidents/*.json'):
            file = open(ref)
            incident = json.load(file)
            file.close()

            risk = incident["type"]
            policy = incident["policy"]
            value = incident[result]

            print str(incident["name"]) + " " + str(value) + " type: " + str(risk)

            # for a policy that has undefined values this returns all possible combinations
            samples = self.generate_samples(policy)

            # add classification last column
            for sample in samples:
                data = policy_model.policy2datapoint(sample)
                data.append(value) # add last column with classification for printing in CSV

                if risk not in entries:
                    entries[risk] = []
                entries[risk].append(data)  # put them in a risk dictionary

        for risk in entries.keys():
            for employee in company.employee_types:
                for location in company.location_types:
                    for device in company.device_types:
                        self.dump_training_set(entries, risk, employee, location, device)

        print "Training set generation for " + self.type + " completed..."

    def dump_training_set(self, entries, risk, employee, location, device):
        #save the risk dictionary files
        context = employee + '-' + location + '-' + device
        tail = 'general' if risk == 'general' else risk + '-' + context

        csv_name = 'static/data/train-' + self.type + '-' + tail + '.csv'
        print csv_name
        writer = csv.writer(open(csv_name, 'w'))
        for row in entries[risk]:
            print row
            writer.writerow(row)

    def generate_samples(self, partial_policy, start_index = 0):
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
                    complete_new = self.generate_samples(new_partial, start_index=i)
                    list.extend(complete_new)

                return list # stop loop when first value is found and recursion for it is done

        return [partial_policy]

    def load_csv_files(self, risk, employee, location, device):
        context = employee+'-'+location+'-'+device
        general = numpy.genfromtxt('static/data/train-' + self.type + '-general.csv', delimiter=',')
        filenames = glob.glob('static/data/train-' + self.type + '-'+risk+'-'+ context +'.csv')

        data = numpy.genfromtxt(filenames[0], delimiter=',')
        data = numpy.concatenate((data, general)) # add positive cases that need to contrast negative ones

        return data

    def train_classifier(self, risk, employee, location, device):
        data = self.load_csv_files(risk, employee, location, device)
        limit = len(policy_model.get_ranges())

        train_data = data[:, 0:limit] # first several columns represent the data dimension
        train_result = data[:, limit] # result columns are ones after data dimensions

        # for explanation of the following parameters please see
        # http://scikit-learn.org/stable/modules/svm.html#tips-on-practical-use
        k = 'rbf'
        cs = 1000
        c = 0.9

        if self.type == 'classifier':
            engine = svm.SVC(kernel=k, cache_size=cs, C=c)
        else:
            engine = svm.SVR(kernel=k, cache_size=cs, C=c)
        model = engine.fit(train_data, train_result)

        return model


if __name__ == "__main__":
    # result = model.generate_samples({'prenew': 3, 'pattempts': 3, 'pdict': 0, 'psets': 2, 'phist': 4})
    # result = model.generate_samples({'plen': 0})
    # result = model.generate_samples({})

    # test_data = genfromtxt('../static/data/pw-test-data.csv', delimiter=',')
    #test_data = [0,0,0,4,0,1,3,1,0]
    # classifier_sklearn.generate_training_set()
    # classifier_sklearn.generate_models()
    #classifier_sklearn.train()
    #test_data = policy_model.get_default()
    #model = classifier_sklearn()
    #filename = 'static/data/pw-train-generated-risk-bruteforce.csv'
    #data = numpy.genfromtxt(filename, delimiter=',')
    #print data

    #print "test data: "
    #print test_data
    #print policy_model.policy2datapoint(test_data)
    #print "classes:"
    #print model.predict_datapoint(test_data)
    trainer_sklearn()
