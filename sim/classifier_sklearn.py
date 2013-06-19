__author__ = 'Daniyar'
from sklearn import svm
from numpy import genfromtxt


class classifier_sklearn:
    def __init__(self):
        train_data = genfromtxt('../static/data/pw-train-data-full.csv', delimiter=',')
        train_result = genfromtxt('../static/data/pw-classifier-classes.csv', delimiter=",")
        self.incidents_model = svm.SVC().fit(train_data, train_result)

    def predict(self, data):
        return self.incidents_model.predict(data)

if __name__ == "__main__":
    test_data = genfromtxt('../static/data/pw-test-data.csv', delimiter=',')
    model = classifier_sklearn()
    print model.predict(test_data)