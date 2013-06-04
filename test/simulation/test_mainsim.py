__author__ = 'Horace'


from sim.simulation import *


class TestMaxSec:

    def test_calc_risk_prob(self):
        policy = simulation()
        policy.set_policy('plen', 8)
        policy.set_policy('psets', 3)
        assert policy.calc_risk_prob() == 0.375

    def test_calc_risk_impact(self):
        policy = simulation()
        assert policy.calc_risk_impact() == 1

    def test_calc_prod_cost(self):
        policy = simulation()
        policy.set_policy('plen', 8)
        policy.set_policy('psets', 3)
        assert policy.calc_prod_cost() == 7


class TestMinSec:

    def test_calc_risk_prob(self):
        policy = simulation()

    def test_calc_risk_impact(self):
        policy = simulation()
        assert policy.calc_risk_impact() == 1

    def test_calc_prod_cost(self):
        policy = simulation()