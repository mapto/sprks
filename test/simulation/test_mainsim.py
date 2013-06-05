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
        assert self.policy.calc_risk_prob() == 0.12

    def test_calc_risk_impact(self):
        assert self.policy.calc_risk_impact() == 1

    def test_calc_prod_cost(self):
        assert self.policy.calc_prod_cost() == 12


class TestMinSec:

    def setup_method(self, method):
        self.policy = simulation()
        self.policy.set_policy('plen', 0)
        self.policy.set_policy('psets', 1)
        self.policy.set_policy('pdict', 0)
        self.policy.set_policy('phist', 0)
        self.policy.set_policy('prenew', 0)
        self.policy.set_policy('pattempts', 0)
        self.policy.set_policy('pautorecover', 1)

    def test_calc_risk_prob(self):
        assert self.policy.calc_risk_prob() == 0.6

    def test_calc_risk_impact(self):
        assert self.policy.calc_risk_impact() == 1

    def test_calc_prod_cost(self):
        assert self.policy.calc_prod_cost() == 1