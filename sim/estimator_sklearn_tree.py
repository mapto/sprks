__author__ = 'mruskov'

from estimator_interface import estimator_interface
from numpy import genfromtxt
from sklearn import tree
import StringIO
import cPickle
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from numpy.random import RandomState
import numpy as np


class estimator_sklearn_tree(estimator_interface):
    def __init__(self):
        # columns in train_data and test CSV file: plen, psets, pdict, phist, prenew, pattempts, pautorecover
        self.name = "full"
        #train_data_conv_risk = self.toNormalized_risk(train_data)
        #train_data_conv_cost = self.toNormalized_cost(train_data)

        train_value = genfromtxt('static/data/pw-train-result-' + self.name + '.csv', delimiter=',')
        print "train value"
        print train_value

        train_data_full = genfromtxt('static/data/pw-train-data-' + self.name + '.csv', delimiter=',')
        self.model_full = tree.DecisionTreeRegressor().fit(train_data_full, train_value)
        train_data_reduced = self.reduceDim(train_data_full, 4)
        self.model_reduced = tree.DecisionTreeRegressor().fit(train_data_reduced, train_value)

        print "train data full"
        print train_data_full
        print "train data reduced"
        print train_data_reduced
        # columns in train_value CSV file and result: risk_prob, risk_impact, prod_cost

        # test_data = genfromtxt('static/data/pw-test-data.csv', delimiter=',')
        """self.risk_prob_model = tree.DecisionTreeRegressor().fit(train_data_conv_risk, train_value[:, 0])
        self.risk_impact_model = tree.DecisionTreeRegressor().fit(train_data_conv_risk, train_value[:, 1])
        self.prod_cost_model = tree.DecisionTreeRegressor().fit(train_data_conv_cost, train_value[:, 2])"""
        # print clf.predict(test_data)
        # use this only if you want to explore what the machine learning algorithm learned
       # self.exportPDF()

    def policy2datapoint(self, policy):
        return [policy["plen"].value(), policy["psets"].value(),
                policy["pdict"].value(), policy["phist"].value(),
                policy["prenew"].value(), policy["pattempts"].value(),
                policy["pautorecover"].value()]

    def policy2datapoint_risk(self, policy):

        """ Policy is a dictionary,
        whereas model accepts an ordered tuple (array)
         """
        complexity = policy["plen"].value() * 3 + policy["psets"].value() * 3 + policy["pdict"].value() * 12 + policy[
        "phist"].value() * 4

        return [complexity,
            policy["prenew"].value() * 16,
            policy["pattempts"].value() * 24,
            policy["pautorecover"].value() * 48]

    def policy2datapoint_cost(self, policy):
        complexity = policy["plen"].value() * 3 + policy["psets"].value() * 3 + policy["pdict"].value() * 12 + policy[
            "phist"].value() * 4
        generator = complexity * policy["prenew"].value() * 16
        memorization = generator + policy["pattempts"].value() * 24
        support = (policy["pattempts"].value() * 24 + memorization) * policy["pautorecover"].value() * 48
        entry = policy["plen"].value() * 3
        return [support, entry, generator, memorization]

    def get_risk_prob(self, policy):
        datapoint = self.policy2datapoint_risk(policy)
        return self.risk_prob_model.predict(datapoint)[0]

    def get_risk_impact(self, policy):
        datapoint = self.policy2datapoint_risk(policy)
        return self.risk_impact_model.predict(datapoint)[0]

    def get_prod_cost(self, policy):
        #datapoint = self.policy2datapoint(policy)
        datapoint = self.policy2datapoint_cost(policy)
        print "cost converted"
        print datapoint
        return self.prod_cost_model.predict(datapoint)[0]

    # calculate weights of dimensions of risk model
    # each dimension carries equal weight of 48
    def toNormalized_risk(self, data):
        arr = []
        for k in data:
            tmp = []
            complexity = k[0] + k[1] * 3 + k[2] * 12 + k[3] * 4
            tmp.append(complexity)
            tmp.append(k[4] * 16)
            tmp.append(k[5] * 24)
            tmp.append(k[6] * 48)
            arr.append(tmp)
        return arr

    # calculate weights of dimensions of cost model

    def toNormalized_cost(self, data):
        arr = []
        for k in data:
            complexity = k[0] + k[1] * 3 + k[2] * 12 + k[3] * 4
            generator = complexity * k[4] * 16
            memorization = generator + k[5] * 24
            support = (k[5] * 24 + memorization) * k[6] * 48
            entry = k[0]
            arr.append([support, entry, generator, memorization])
        return arr

    def generateAllPolicies(self):
        plen = [0, 6, 8, 10, 12]
        psets = [1, 2, 3, 4]
        pdict = [0, 1]
        phist = [0, 1, 2, 3]
        prenew = [0, 1, 2, 3]
        pattempts = [0, 1, 2]
        pautorec = [0, 1]

        arr = []

        for plen_v in plen:
            for psets_v in psets:
                for pdict_v in pdict:
                    for phist_v in phist:
                        for prenew_v in prenew:
                            for pattempts_v in pattempts:
                                for pautorec_v in pautorec:
                                    tmp = [plen_v, psets_v, pdict_v, phist_v, prenew_v, pattempts_v, pautorec_v]
                                    arr.append(tmp)
        return arr

    def getClusters(self, data):
        rnd = RandomState(42)
        kmeans = KMeans(n_clusters=9, random_state=rnd)
        kmeans.fit(data)
        return np.round(kmeans.cluster_centers_, decimals=2)

    def reduceDim(self, data, new_dim):
       # PCA = __import__('sklearn.decomposition.PCA')
        pca = PCA(new_dim, whiten=True)
        pca.fit(data)
        data_pca = pca.transform(data)
        print data_pca.shape
        return data_pca


    def exportPDF(self):
        """ Use this to export a visual representation of the learned model
                requires graphviz (http://www.graphviz.org) and pydot to be installed
            """
        dot_data = StringIO.StringIO()

        try:
            pydot = __import__('pydot')

            """ tree.export_graphviz(self.risk_prob_model, out_file=dot_data)
            graph = pydot.graph_from_dot_data(dot_data.getvalue())
            graph.write_pdf("static/data/tree-" + self.name + "-risk-prob.pdf")"""
            #
            # tree.export_graphviz(self.risk_impact_model, out_file=dot_data)
            # graph = pydot.graph_from_dot_data(dot_data.getvalue())
            # graph.write_pdf("static/data/tree-" + self.name + "-risk-impact.pdf")
            #
            """tree.export_graphviz(self.prod_cost_model, out_file=dot_data)
            graph = pydot.graph_from_dot_data(dot_data.getvalue())
            graph.write_pdf("static/data/tree-" + self.name + "-prod-cost.pdf")"""
            tree.export_graphviz(self.model, out_file=dot_data)
            graph = pydot.graph_from_dot_data(dot_data.getvalue())
            graph.write_pdf("static/data/tree-" + self.name + ".pdf")

            #

        except ImportError:
            # If pydot not installed (*cough Travis *cough), silently fail...
            pass

    def predict(self, datapoints):
        """ return [self.risk_prob_model.predict(datapoints),
                self.risk_impact_model.predict(datapoints),
                self.prod_cost_model.predict(datapoints)]"""
        return self.model.predict(datapoints)


if __name__ == "__main__":
#  understand this:
#  http://scikit-learn.org/stable/auto_examples/tree/plot_tree_regression_multioutput.html#example-tree-plot-tree-regression-multioutput-py
    import os

    os.chdir("..")
    tool = estimator_sklearn_tree()
    #test_data = genfromtxt('static/data/pw-test-data.csv', delimiter=',')
    data = tool.generateAllPolicies()
    data_conv = tool.toNormalized_risk(data)
    print tool.getClusters(data_conv)
    """print test_data
    print "reduced data"
    tst_data = tool.reduceDim(test_data, 4)
    print tst_data"""
    #test_data_conv = tool.toNormalized_cost(test_data)
    #print test_data_conv
    """ print "from full model"
    print tool.model_full.predict(test_data)
    print "from reduced model"
    print tool.model_reduced.predict(tst_data)"""
   # print "predicted data"
   # print tool.prod_cost_model.predict(test_data_conv)
#    tool.risk_impact_model.predict(datapoints)
#    tool.prod_cost_model.predict(datapoints)