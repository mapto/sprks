from policy_plen import policy_plen
from policy_psets import policy_psets

__author__ = 'Horace'


class simulation:
    def set_policy(self, policy_name, policy_value):
        """Sets a parameter to the user policy.

        Possible parameters are (for meanings check specific policy classes):
        plen: {0, 6, 8, 10, 12}
        psets: {1, 2, 3, 4}
        pdict: {True, False}
        phist: {0, 1, 2, 3}
        prenew: {0, 1, 2, 3}
        pattempts: {True, False}
        pautorecover: {True, False}
        """
        # policy_class = getattr(__thismodule__, policy_name)
#        if not policy_instance isinstance(policy_interface)
        # policy_instance = policy_class(policy_value)

        # Risk probability and impact are multiplied together
        # Productivity costs are added together
        # TODO parse policy parameters and dynamically create policy items
#        self.dict = {}
#        self.dict['plen'] = policy_plen(8)
#        self.dict['psets'] = policy_psets(3)

        runtime_class = "policy_" + str(policy_name)
#        print runtime_class + "[" + policy_name + "] = " + str(policy_value)
        constructor = globals()[runtime_class]
        if not hasattr(self, 'dict'): self.dict = {} # lasy initialization of policies dictionary
        self.dict[policy_name] = constructor(policy_value)

        return 0

    def calc_risk_prob(self):
        result = 1
        for value in self.dict.values():
            result = result * value.get_risk_prob()
        return result

    def calc_risk_impact(self):
        return 1

    def calc_prod_cost(self):
        result = 0
        for value in self.dict.values():
            result = result + value.get_prod_cost()
        return result


