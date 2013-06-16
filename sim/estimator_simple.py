__author__ = 'mruskov'

from estimator_interface import estimator_interface

class estimator_simple(estimator_interface):
    def __init__(self):
        """ Nothing to be done here
        """

    def get_risk_prob(self, policies):
        risk = 1
        for policy in policies:
            risk *= policies[policy].get_risk_prob()
        return risk

    def get_risk_impact(self, policies):
        impact = 1
        for policy in policies:
            impact *= policies[policy].get_risk_impact()
        return impact

    def get_prod_cost(self, policies):
        cost = 0
        for policy in policies:
            cost += policies[policy].get_prod_cost()
        return cost
