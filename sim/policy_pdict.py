import policy_interface

__author__ = 'Horace'


class policy_pdict(policy_interface.policy_interface):
    def __init__(self):
        self.__init__(0)

    def __init__(self, value):
        if value in [0, 1]:
            self.param = value
        else:
            raise Exception('Wrong parameter type')

    def get_risk_prob(self):

        if self.param == 1:
            return .4
        else:
            return .6

    def get_risk_impact(self):
        return 1 # need a value that does not affect the formula

    def get_prod_cost(self):

        if self.param == 1:
            return 2
        else:
            return 1
