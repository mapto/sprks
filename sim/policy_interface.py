__author__ = 'Horace'


class policy_interface:
    def __init__(self, value):
        self.param = Exception('Parameter not set')
        raise NotImplementedError('Unknown policy')

    def value(self):
        return self.param

    def get_risk_prob(self, x):
        """Probability multiplier for network intrusion risk assuming worst case (easiest to attack) for other variables
        """
        raise NotImplementedError('Unknown policy')

    def get_risk_impact(self, x):
        """Impact multiplier for network intrusion risk caused by decisions of this policy
        """
        raise NotImplementedError('Unknown policy')

    def get_prod_cost(self, x):
        """Productive minutes lost per week due to this policy
        """
        raise NotImplementedError('Unknown policy')

