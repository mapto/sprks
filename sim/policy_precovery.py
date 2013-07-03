import policy_interface

__author__ = 'Horace'


class policy_precovery(policy_interface.policy_interface):
    # whether passwords can be recovered without human contact
    def __init__(self):
        self.__init__(0)

    def __init__(self, value):

        value = int(value)

        if value in [0, 1, 2]:
            self.param = (value != 0)
        else:
            raise Exception('Wrong parameter type')

    def get_risk_prob(self):

        if self.param == 1:
            return .6
        else:
            return .2

    def get_risk_impact(self):
        return 1 # need a value that does not affect the formula

    def get_prod_cost(self):

        if self.param == 1:
            return 1
        else:
            return 10
