__author__ = 'mruskov'

from estimator_interface import estimator_interface
from numpy import genfromtxt
from sklearn import tree
import pydot # if you don't have pydot installed comment out this line and the exportFDF() method
import StringIO


class estimator_sklearn_tree(estimator_interface):
    def __init__(self):
        # columns in train_data and test CSV file: plen, psets, pdict, phist, prenew, pattempts, pautorecover
        self.name = "full"
        train_data = genfromtxt('static/data/pw-train-data-' + self.name + '.csv', delimiter=',')
        # columns in train_value CSV file and result: risk_prob, risk_impact, prod_cost
        train_value = genfromtxt('static/data/pw-train-result-' + self.name + '.csv', delimiter=',')
        # test_data = genfromtxt('static/data/pw-test-data.csv', delimiter=',')
        self.risk_prob_model = tree.DecisionTreeRegressor().fit(train_data, train_value[:, 0])
        self.risk_impact_model = tree.DecisionTreeRegressor().fit(train_data, train_value[:, 1])
        self.prod_cost_model = tree.DecisionTreeRegressor().fit(train_data, train_value[:, 2])
        # print clf.predict(test_data)

    # use this only if you want to explore what the machine learning algorithm learned
        self.exportPDF()

    def policy2datapoint(self, policy):
        """ Policy is a dictionary,
            whereas model accepts an ordered tuple (array)
        """
        return [policy["plen"].value(),
                policy["psets"].value(),
                policy["pdict"].value(),
                policy["phist"].value(),
                policy["prenew"].value(),
                policy["pattempts"].value(),
                policy["pautorecover"].value()]

    def get_risk_prob(self, policy):
        datapoint = self.policy2datapoint(policy)
        return self.risk_prob_model.predict(datapoint)[0]

    def get_risk_impact(self, policy):
        datapoint = self.policy2datapoint(policy)
        return self.risk_impact_model.predict(datapoint)[0]

    def get_prod_cost(self, policy):
        datapoint = self.policy2datapoint(policy)
        return self.prod_cost_model.predict(datapoint)[0]

    def exportPDF(self):
        """ Use this to export a visual representation of the learned model
            requires graphviz (http://www.graphviz.org) and pydot to be installed
        """
        dot_data = StringIO.StringIO()

        tree.export_graphviz(self.risk_prob_model, out_file=dot_data)
        graph = pydot.graph_from_dot_data(dot_data.getvalue())
        #graph.write_pdf("static/data/tree-" + self.name + "-risk-prob.pdf")
        """
        tree.export_graphviz(self.risk_impact_model, out_file=dot_data)
        graph = pydot.graph_from_dot_data(dot_data.getvalue())
        graph.write_pdf("static/data/tree-" + self.name + "-risk-impact.pdf")

        tree.export_graphviz(self.prod_cost_model, out_file=dot_data)
        graph = pydot.graph_from_dot_data(dot_data.getvalue())
        graph.write_pdf("static/data/tree-" + self.name + "-prod-cost.pdf")
        """

    def predict(self, datapoints):
        return [self.risk_prob_model.predict(datapoints),
                self.risk_impact_model.predict(datapoints),
                self.prod_cost_model.predict(datapoints)]


if __name__ == "__main__":
#  understand this:
#  http://scikit-learn.org/stable/auto_examples/tree/plot_tree_regression_multioutput.html#example-tree-plot-tree-regression-multioutput-py
    import os

    os.chdir("..")
    tool = estimator_sklearn_tree()
    test_data = genfromtxt('static/data/pw-test-data.csv', delimiter=',')
    print test_data
    print tool.predict(test_data)