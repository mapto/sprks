__author__ = 'Daniyar'

from sklearn import svm
import numpy
import glob
from models.incident import incident
import json
from models.pw_policy import pw_policy_model as pw_policy


class classifier_sklearn:
    def __init__(self):
        self.incidents_models = {}
        self.risks = []
        general = numpy.genfromtxt('static/data/pw-train-generated-general.csv', delimiter=',')
        for filename in glob.glob('static/data/pw-train-generated-risk-*.csv'):
            risk = filename[36:-4] # take actual name
            self.risks.append(risk)
            # data = genfromtxt('static/data/pw-train-estimator-risk-' + risk + '.csv', delimiter=',')
            data = numpy.genfromtxt(filename, delimiter=',')
            data = numpy.concatenate((data, general)) # add positive cases that need to contrast negative ones
            train_data = data[:, 0:7] # first 7 columns
            train_result = data[:, 7] # last columns after 7
            self.incidents_models[risk] = svm.SVC().fit(train_data, train_result)
            # self.incidents_models[risk] = svm.SVR().fit(train_data, train_result)

        # print self.risks

    def predict_data(self, data):
        datapoints = pw_policy.policy2datapoint(data)
        return self.predict_datapoint(datapoints)

    def predict_datapoint(self, datapoints):
        greatest = None

        risks_list = {}

        for risk in self.risks:
            cls = self.incidents_models[risk].predict(datapoints)[0]
            cls = int(cls) # algorithm returns float, we need to match it to string defined in json
            # data is returned as an array of numpy.float64, we need integers so we could use them as incident indices
            # event = incident(cls[0].astype(int64))
            # risk = event.get_risk()
            event = incident.get_incident(cls)

            risks_list[risk] = event["risk"]

            #if greatest is None or event["risk"] > greatest[1]:
            #   greatest = [event["name"], event["risk"]] # 0 - name, 1 - risk

        return risks_list
        #return self.incidents_model.predict(data)


if __name__ == "__main__":
    # test_data = genfromtxt('../static/data/pw-test-data.csv', delimiter=',')
    test_data = [6, 2, 1, 1, 2, 0, 1]
    model = classifier_sklearn()
    print "test data: "
    print test_data
    print "classes:"
    print model.predict_datapoint(test_data)