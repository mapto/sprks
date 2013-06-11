import policy_interface

__author__ = 'Horace'

class policy_pdict(policy_interface.policy_interface):
    def __init__(self):
        self.__init__(3)

    def __init__(self, value):
        if type(value) == bool:
            self.param = value
        else:
            raise Exception('Wrong parameter type')

    def get_risk_prob(self):

        if self.param:
            return .4
        else:
            return .6

    def get_risk_impact(self):
        return 1 # need a value that does not affect the formula

    def get_prod_cost(self):

        if self.param:
            return 2
        else:
            return 1
