__author__ = 'Horace'


class simulation:
    def set_policy(self, policy_name, policy_value):
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

        # Risk probability and impact are multiplied together
        # Productivity costs are added together
        # TODO parse policy parameters and dynamically create policy items
        # TODO import all classes from all sim moduless

        if not hasattr(self, 'dict'):
            # lazy initialization of policies dictionary
            self.dict = {}
        self.dict[policy_name] = self.load_policy(policy_name)(policy_value)
        return 0

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
        return self.dict['plen'].get_risk_prob() * self.dict['psets'].get_risk_prob()

    def calc_risk_impact(self):
        return 1

    def calc_prod_cost(self):
        return self.dict['plen'].get_prod_cost() + self.dict['psets'].get_prod_cost()