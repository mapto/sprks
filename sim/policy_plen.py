import policy_interface

__author__ = 'Horace'

class policy_plen(policy_interface.policy_interface):
    def __init__(self):
        self.__init__(3)

    def __init__(self, value):
        if value in [0, 6, 8, 10, 12]:
            self.param = value
        else:
            raise Exception('Wrong parameter type')
    def get_risk_prob(self):

        return {
            0: 1,
            6: .9,
            8: .75,
            10: .6,
            12: .4,
        }[self.param]

    def get_risk_impact(self):
        return 1 # need a value that does not affect the formula

    def get_prod_cost(self):
        return {
            0: 1,
            6: 4,
            8: 5,
            10: 6,
            12: 7,
        }[self.param]
