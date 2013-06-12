import policy_interface

__author__ = 'Horace'

class policy_prenew(policy_interface.policy_interface):
    def __init__(self):
        self.__init__(3)

    def __init__(self, value):

        value = int(value)

        if value in [0, 1, 2, 3]:
            # never, annual, quarterly, monthly
            self.param = value
        else:
            raise Exception('Wrong parameter type')

    def get_risk_prob(self):

        return {
            0: .9,
            1: .3,
            2: .2,
            3: .1,
        }[self.param]

    def get_risk_impact(self):
        return 1 # need a value that does not affect the formula

    def get_prod_cost(self):
        return {
            0: 0,
            1: 0,
            2: 1,
            3: 2,
        }[self.param]
