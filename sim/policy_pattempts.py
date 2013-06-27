import policy_interface

__author__ = 'Horace'


class policy_pattempts(policy_interface.policy_interface):
    # whether or not there's a limit to number of attempts before user is locked out
    def __init__(self):
        self.__init__(0)

    def __init__(self, value):

        value = int(value)

        if value in [0, 1, 2]:
            #self.param = (value != 0)
            self.param = value
        else:
            raise Exception('Wrong parameter type')

    def get_risk_prob(self):

        if self.param == 1:
            return .3
        elif self.param == 2:
            return .5
        else:
            return .8

    def get_risk_impact(self):
        return 1 # need a value that does not affect the formula

    def get_prod_cost(self):

        if self.param == 1:
            return 10
        elif self.param == 2:
            return 5
        else:
            return 1
