import policy_interface

__author__ = 'Horace'

class policy_psets(policy_interface.policy_interface):
    def __init__(self):
        self.__init__(3)

    def __init__(self, value):
        if value in [1, 2, 3, 4]:
            self.param = value
        else:
            raise Exception('Wrong parameter type')
    def get_risk_prob(self):

        return {
            1: .6,
            2: .55,
            3: .5,
            4: .3,
        }[self.param]

    def get_risk_impact(self):
        return 1 # need a value that does not affect the formula

    def get_prod_cost(self):
        return {
            1: 0,
            2: 1,
            3: 2,
            4: 5,
        }[self.param]
