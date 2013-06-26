__author__ = 'Daniyar'
from sklearn import svm
from numpy import genfromtxt
from models.incident import incident
import json


class classifier_sklearn:
    def __init__(self):
        train_data = genfromtxt('../static/data/pw-train-data-full.csv', delimiter=',')
        train_result = genfromtxt('../static/data/pw-train-result-classifier-full.csv', delimiter=",")
        self.incidents_model = svm.SVC().fit(train_data, train_result)

    def predict(self, data):
        cls = self.incidents_model.predict(data)
        return json.dumps([incident().get_incident_risk(cls),
                           incident().get_incident_cost(cls),
                           incident().get_incident_description(cls)])
        #return self.incidents_model.predict(data)


if __name__ == "__main__":
    test_data = genfromtxt('../static/data/pw-test-data.csv', delimiter=',')
    model = classifier_sklearn()
    print "test data:"
    print test_data
    print "classes:"
    print model.predict(test_data)