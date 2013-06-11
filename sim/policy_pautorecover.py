import policy_interface

__author__ = 'Horace'

class policy_pautorecover(policy_interface.policy_interface):
    # whether passwords can be recovered without human contact
    def __init__(self):
        self.__init__(3)

    def __init__(self, value):
        if type(value) == bool:
            self.param = value
        elif type(value) == int:
            self.param = (value != 0)
        else:
            raise Exception('Wrong parameter type')

    def get_risk_prob(self):

        if self.param:
            return .6
        else:
            return .2

    def get_risk_impact(self):
        return 1 # need a value that does not affect the formula

    def get_prod_cost(self):

        if self.param:
            return 1
        else:
            return 10
