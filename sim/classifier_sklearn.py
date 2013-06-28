__author__ = 'Daniyar'
from sklearn import svm
from numpy import genfromtxt
from numpy import int64
from models.incident import incident
import json


class classifier_sklearn:
    def __init__(self):
        self.incidents_models = {}

        train_data_bfa = genfromtxt('static/data/pw-train-data-full.csv', delimiter=',')
        train_result_bfa = genfromtxt('static/data/pw-train-result-classifier-full.csv', delimiter=",")
        self.incidents_models["bfa"] = svm.SVC().fit(train_data_bfa, train_result_bfa)

        train_data_thft = genfromtxt('static/data/pw-train-data-stolen.csv', delimiter=',')
        train_result_thft = genfromtxt('static/data/pw-train-result-classifier-stolen.csv', delimiter=",")
        self.incidents_models["thft"] = svm.SVC().fit(train_data_thft, train_result_thft)

    def policy2datapoint(self, policy):
        return [policy["plen"].value(), policy["psets"].value(),
                policy["pdict"].value(), policy["phist"].value(),
                policy["prenew"].value(), policy["pattempts"].value(),
                policy["pautorecover"].value()]

    def predict(self, data):
        datapoints = self.policy2datapoint(data)
        cls_bfa = self.incidents_models["bfa"].predict(datapoints)
        cls_thft = self.incidents_models["thft"].predict(datapoints)
        # data is returned as numpy.float64, we need integers so we could use them as incident indices
        event_bfa = incident(cls_bfa[0].astype(int64))
        event_thft = incident(cls_thft[0].astype(int64))

        bfa_risk = event_bfa.get_risk()
        thft_risk = event_thft.get_risk()

        if bfa_risk >= thft_risk:
            risk = bfa_risk
            cost = event_bfa.get_cost()
            description = event_bfa.get_description()
        else:
            risk = thft_risk
            cost = event_thft.get_cost()
            description = event_thft.get_description()

        return [risk, cost, description]
        #return self.incidents_model.predict(data)


if __name__ == "__main__":
    #test_data = genfromtxt('../static/data/pw-test-data.csv', delimiter=',')
    test_data = [6, 2, 1, 1, 2, 0, 1]
    model = classifier_sklearn()
    print "test data:"
    print test_data
    print "classes:"
    print model.predict(test_data)