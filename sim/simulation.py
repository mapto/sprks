from policy_plen import policy_plen
from policy_psets import policy_psets

__author__ = 'Horace'


class simulation:
    def set_policy(self, policy_name, policy_value):
        # policy_class = getattr(__thismodule__, policy_name)
#        if not policy_instance isinstance(policy_interface)
        # policy_instance = policy_class(policy_value)

        # Risk probability and impact are multiplied together
        # Productivity costs are added together
        # TODO parse policy parameters and dynamically create policy items
        self.dict = {}
        self.dict['plen'] = policy_plen(8)
        self.dict['psets'] = policy_psets(3)
        return 0

    def calc_risk_prob(self):
        return self.dict['plen'].get_risk_prob() * self.dict['psets'].get_risk_prob()

    def calc_risk_impact(self):
        return 1

    def calc_prod_cost(self):
        return self.dict['plen'].get_prod_cost() + self.dict['psets'].get_prod_cost()

policy = simulation()
policy.set_policy('plen', 8)
policy.set_policy('psets', 3)
print policy.calc_risk_prob()
print policy.calc_prod_cost()

