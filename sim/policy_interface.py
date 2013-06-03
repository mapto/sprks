__author__ = 'Horace'

class policy_interface:
    param = Exception('Parameter not set')
    def __init__(self, value):
        raise NotImplementedError('Unknown policy')
    def __init__(self):
        raise Exception('Missing parameter')
    def get_risk_prob(self, x):
        # probability multiplier for network intrusion risk assuming worst case (easiest to attack) for other variables
        raise NotImplementedError('Unknown policy')
    def get_risk_impact(self, x):
        # impact multiplier for network intrusion risk caused by decisions of this policy
        raise NotImplementedError('Unknown policy')
    def get_prod_cost(self, x):
        # productive minutes lost per week due to this policy
        raise NotImplementedError('Unknown policy')

