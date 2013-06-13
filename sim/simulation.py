__author__ = 'Horace'


class simulation:

    def __init__(self, policies = {}):
        if not hasattr(self, 'dict'):
        # lazy initialization of policies dictionary
            self.dict = {}
        self.set_multi_policy(policies)

    def set_multi_policy(self, policies):
        """
        Accept policy as dict.
        """
        #for k, v in policies.iteritems():
         #   self.set_policy(k, v)
        self.set_policy(policies)

    #def set_policy(self, policy_name, policy_value):
    def set_policy(self, data):
        """
        Sets a parameter to the user policy.

        Possible parameters are (for meanings check specific policy classes):
        plen: {0, 6, 8, 10, 12}
        psets: {1, 2, 3, 4}
        pdict: {True, False}
        phist: {0, 1, 2, 3}
        prenew: {0, 1, 2, 3}
        pattempts: {True, False}
        pautorecover: {True, False}
        """
        #converted_data = eval(data)
        # Risk probability and impact are multiplied together
        # Productivity costs are added together
        for k, value in data.iteritems():
            self.dict[k] = self.load_policy(k)(value)

    def load_policy(self, policy_name):
        """
        If required policy class is already loaded, returns it.
        Otherwise imports the module and the class within.
        """

        policy_id = "policy_" + policy_name
        if policy_id in globals():
            return globals()[policy_id]
        else:
            # lazy class loading
            policy_module = __import__('sim.' + policy_id)
            # weird hack... no idea why we need getattr twice...
            return getattr(getattr(policy_module, policy_id), policy_id)

    def calc_risk_prob(self):
        risk = 1
        for policy in self.dict:
            risk *= self.dict[policy].get_risk_prob()
        return round(risk, 2)

    def calc_risk_impact(self):
        impact = 1
        for policy in self.dict:
            impact *= self.dict[policy].get_risk_impact()
        return round(impact, 2)

    def calc_prod_cost(self):
        cost = 0
        for policy in self.dict:
            cost += self.dict[policy].get_prod_cost()
        return round(cost, 0)