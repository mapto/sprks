import policy_interface

__author__ = 'Horace'

class policy_psets(policy_interface.policy_interface):
    def __init__(self):
        self.__init__(3) # default value for constructor with parameter

    def __init__(self, value):
        """Specifies the number of symbol sets required for passwords.
        1 means only lowercase required
        2 means require both uppercase and lowercase
        3 require also numbers
        4 require special symbols

        Parameter -- the sets required.
        Default value is 3.
        """
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
