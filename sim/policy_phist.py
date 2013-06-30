import policy_interface

__author__ = 'Horace'


class policy_phist(policy_interface.policy_interface):
    def __init__(self):
        self.__init__(3)

    def __init__(self, value):

        value = int(value)

        if value in [0, 1, 2, 3]:
            self.param = value
        else:
            raise Exception('Wrong parameter type')

    def get_risk_prob(self):

        return {
            0: .8,
            1: .6,
            2: .4,
            3: .3,
        }[self.param]

    def get_risk_impact(self):
        return 1 # need a value that does not affect the formula

    def get_prod_cost(self):
        return {
            0: 0,
            1: 3,
            2: 5,
            3: 10,
        }[self.param]
