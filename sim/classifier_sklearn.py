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

    def __init__(self):
        """
        Initializes all implicit models.
        Currently there is one model per risk,
        but should turn into one model per risk per environmental configuration
        :param user_id:
        :param sync_date:
        """
        self.incidents_models = {}
        self.risks = []
        check_classifier = True
        f = open('static/data/classifier-models.txt','rb')
        self.incidents_models = cPickle.load(f)
        f.close()


    @staticmethod
    def train():
        """This is the main method creating the implicit model, based on the provided incidents
           It takes the incidents in static/incidents/*,json as input
           and generates static/data/classifier-models.pkl as output.
           This model is a serialization of the trained/fitted model
           Currently the CSV training set in static/data/train-generated*.csv is a by-product, but is not really needed
        """
        classifier_sklearn.generate_training_set()
        classifier_sklearn.generate_models()

    @staticmethod
    def generate_models():
        """ Train the SVM models from the CSV dataset

        """
        print "Generating models..."

        f = open('static/data/classifier-models.txt', 'wb')

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
                        models[risk][employee][location][device] = classifier_sklearn.train_classifier(risk, employee, location, device)

        cPickle.dump(models, f)
        f.close()
        print "Model generation completed..."


    @staticmethod
    def generate_training_set():
        """
        Generalizes the incidents into a training set to be used by the implicit model.
        This assumes the types of risks
        """

        # this is iteration of incidents, values are specified in data
        print "Generating training set..."
        entries = {}

        # read incidents and generate training sets
        for ref in glob.glob('static/incidents/*.json'):
            file = open(ref)
            incident = json.load(file)
            file.close()

            risk = incident["type"]
            policy = incident["policy"]
            cls = incident["id"]

            print str(incident["name"]) + " " + str(cls) + " type: " + str(risk)

            # for a policy that has undefined values this returns all possible combinations
            samples = classifier_sklearn.generate_samples(policy)

            # add classification last column
            for sample in samples:
                data = policy_model.policy2datapoint(sample)
                data.append(cls) # add last column with classification for printing in CSV

                if risk not in entries:
                    entries[risk] = []
                entries[risk].append(data)  # put them in a risk dictionary

        for risk in entries.keys():
            for employee in company.employee_types:
                for location in company.location_types:
                    for device in company.device_types:
                        classifier_sklearn.dump_training_set(entries, risk, employee, location, device)

        print "Training set generation completed..."

    @staticmethod
    def dump_training_set(entries, risk, employee, location, device):
        #save the risk dictionary files
        context = employee + '-' + location + '-' + device
        tail = 'general' if risk == 'general' else risk + '-' + context

        csv_name = 'static/data/train-generated-' + tail + '.csv'
        print csv_name
        writer = csv.writer(open(csv_name, 'w'))
        for row in entries[risk]:
            print row
            writer.writerow(row)

    @staticmethod
    def generate_samples(partial_policy, start_index = 0):
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
                    complete_new = classifier_sklearn.generate_samples(new_partial, start_index=i)
                    list.extend(complete_new)

                return list # stop loop when first value is found and recursion for it is done

        return [partial_policy]

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

    @staticmethod
    def load_csv_files(risk, employee, location, device):
        context = employee+'-'+location+'-'+device
        general = numpy.genfromtxt('static/data/train-generated-general.csv', delimiter=',')
        filenames = glob.glob('static/data/train-generated-'+risk+'-'+ context +'.csv')

        data = numpy.genfromtxt(filenames[0], delimiter=',')
        data = numpy.concatenate((data, general)) # add positive cases that need to contrast negative ones

        return data

    @staticmethod
    def train_classifier(risk, employee, location, device):
        data = classifier_sklearn.load_csv_files(risk, employee, location, device)
        limit = len(policy_model.get_ranges())

        train_data = data[:, 0:limit] # first several columns represent the data dimension
        train_result = data[:, limit] # result columns are ones after data dimensions

        # for explanation of the following parameters please see
        # http://scikit-learn.org/stable/modules/svm.html#tips-on-practical-use
        return svm.SVC(kernel='rbf', cache_size=1000, C=0.9).fit(train_data, train_result)

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
    classifier_sklearn.train()
