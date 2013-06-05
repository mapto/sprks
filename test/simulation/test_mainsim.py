__author__ = 'Horace'


from sim.simulation import *


class TestMaxSec:

    def setup_method(self, method):
        self.policy = simulation()
        self.policy.set_policy('plen', 12)
        self.policy.set_policy('psets', 4)
        self.policy.set_policy('pdict', 1)
        self.policy.set_policy('phist', 1)
        self.policy.set_policy('prenew', 3)
        self.policy.set_policy('pattempts', 1)
        self.policy.set_policy('pautorecover', 0)

    def test_calc_risk_prob(self):
        assert self.policy.calc_risk_prob() == 0.375

    def test_calc_risk_impact(self):
        assert self.policy.calc_risk_impact() == 1

    def test_calc_prod_cost(self):
        assert self.policy.calc_prod_cost() == 7


class TestMinSec:

    def test_calc_risk_prob(self):
        policy = simulation()

    def test_calc_risk_impact(self):
        policy = simulation()
        assert policy.calc_risk_impact() == 1

    def test_calc_prod_cost(self):
        policy = simulation()