__author__ = 'Daniyar'

from sklearn import svm
import numpy
import glob
from models.incident import incident
import json
from models.pw_policy import pw_policy_model as pw_policy
from models.company import company


class classifier_sklearn:
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
        self.risks_set = ["bruteforce", "stolen"]

        """ Currently the data model in the simulation is dependent on pw_policy
            This should be generalized and made dependent on policies
        """
        limit = len(pw_policy.ranges)

        general = numpy.genfromtxt('static/data/pw-train-generated-general.csv', delimiter=',')

        """ for filename in glob.glob('static/data/pw-train-generated-risk-*.csv'):
            risk = filename[36:-4] # take actual name
            self.risks.append(risk)
            # data = genfromtxt('static/data/pw-train-estimator-risk-' + risk + '.csv', delimiter=',')
            data = numpy.genfromtxt(filename, delimiter=',')
            data = numpy.concatenate((data, general)) # add positive cases that need to contrast negative ones
            train_data = data[:, 0:limit] # first several columns represent the data dimension
            train_result = data[:, limit] # result columns are ones after data dimensions
            self.incidents_models[risk] = svm.SVC().fit(train_data, train_result)
        """

        for risk in self.risks_set:
            if not risk in self.incidents_models.keys():
                self.incidents_models[risk] = {}
            for employee in company.employee_types:
                if not employee in self.incidents_models[risk].keys():
                    self.incidents_models[risk][employee] = {}
                for location in company.location_types:
                    if not location in self.incidents_models[risk][employee].keys():
                        self.incidents_models[risk][employee][location] = {}
                    for device in company.device_types:
                        if not device in self.incidents_models[risk][employee][location].keys():
                            self.incidents_models[risk][employee][location][device] = {}
                        self.incidents_models[risk][employee][location][device] = self.generate_training_data(risk, employee, location, device, limit, general)
            # self.incidents_models[risk] = svm.SVR().fit(train_data, train_result)

        # print self.risks

    def predict_data(self, data):
        """
        Makes a prediction for a particular policy
        Currently only handles pw_policy, but in future data preparation needs to be handled by the model.
        :param data: The policy configuration that needs to be consistent with the used data structure
        """
        datapoints = pw_policy.policy2datapoint(data)
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
        for risk in self.risks_set:
            my_list = []
            for employee in company.employee_types:
                for location in company.location_types:
                    for device in company.device_types:
                        cls = self.incidents_models[risk][employee][location][device].predict(datapoints)[0]
                        cls = int(cls) # algorithm returns float, we need to match it to string defined in json
                        # data is returned as an array of numpy.float64, we need integers so we could use them as incident indices
                        # event = incident(cls[0].astype(int64))
                        # risk = event.get_risk()
                        event = incident.get_incident(cls)
                        my_list.append(event['id'])
                        #risks_list.append(event["id"])
            tmp_list[risk] = my_list
            #if greatest is None or event["risk"] > greatest[1]:
            #   greatest = [event["name"], event["risk"]] # 0 - name, 1 - risk

        max = 1
        for risk in tmp_list:
            for value in tmp_list[risk]:
                if value < max:
                    max = value
            risks_list.append(max)
            max = 1

        return risks_list
        #return self.incidents_model.predict(data)

    def generate_training_data(self, risk, employee, location, device, limit, general):
        filename = glob.glob('static/data/pw-train-generated-'+risk+'-'+employee+location+device+'.csv')
        data = numpy.genfromtxt(filename, delimiter=',')
        data = numpy.concatenate((data, general)) # add positive cases that need to contrast negative ones
        train_data = data[:, 0:limit] # first several columns represent the data dimension
        train_result = data[:, limit] # result columns are ones after data dimensions
        return svm.SVC().fit(train_data, train_result)


if __name__ == "__main__":
    # test_data = genfromtxt('../static/data/pw-test-data.csv', delimiter=',')
    test_data = [6, 2, 1, 1, 2, 0, 1]
    model = classifier_sklearn()
    print "test data: "
    print test_data
    print "classes:"
    print model.predict_datapoint(test_data)