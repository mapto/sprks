import policy_interface

__author__ = 'Horace'

class policy_plen(policy_interface.policy_interface):
    def __init__(self):
        self.__init__(6) # default value for constructor with parameter

    def __init__(self, value):
        """Sets the minimum password length

        Parameter -- the minimum password length. 0 means disabled, i.e. allowing empty passwords
        Default value is 6
        """

        value = int(value)

        if value in [0, 1, 2, 3, 4]:
            self.param = value
        else:
            raise Exception('Invalid policy parameter.')

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
