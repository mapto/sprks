__author__ = 'mruskov'

class estimator_interface:
    def __init__(self):
        """ Use this to load the training set of your policy
        """
        raise NotImplementedError('Unknown estimator')

    def get_risk_prob(self, policy):
        raise NotImplementedError('Unknown estimator')

    def get_risk_impact(self, policy):
        raise NotImplementedError('Unknown estimator')

    def get_prod_cost(self, policy):
        raise NotImplementedError('Unknown estimator')