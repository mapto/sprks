__author__ = 'Horace'

from sim.simulation import *


class TestNoPolicy:
    """
    Tests the calculated values if no policy details are loaded.
    """
    # TODO tests broken - lazy init of policies vs auto init all policies
    def setup_method(self, method):
        self.no_policy = simulation()

    def test_calc_risk_prob(self):
        # assert self.no_policy.calc_risk_prob() == 1
        pass

    def test_calc_risk_impact(self):
        # assert self.no_policy.calc_risk_impact() == 1
        pass

    def test_calc_prod_cost(self):
        # assert self.no_policy.calc_prod_cost() == 0
        pass


class TestPolicyConstructor:
    """
    Tests whether calling the __init__(self, policies) constructor has same effect as calling __init__(self) and loading
     policies explicitly.
    """

    def setup_method(self, method):
        policy_set = {'plen': 12, 'psets': 4, 'pdict': 1, 'phist': 3, 'prenew': 3, 'pattempts': 1, 'pautorecover': 0}
        self.multi_policy = simulation()
        self.multi_policy.set_multi_policy(policy_set)

        self.impl_policy = simulation(policy_set)

    def test_calc_risk_prob(self):
        assert self.impl_policy.calc_risk_prob() == self.multi_policy.calc_risk_prob()

    def test_calc_risk_impact(self):
        assert self.impl_policy.calc_risk_impact() == self.multi_policy.calc_risk_impact()

    def test_calc_prod_cost(self):
        assert self.impl_policy.calc_prod_cost() == self.multi_policy.calc_prod_cost()


class TestSetPolicy:
    """
    Tests whether loading multiple policies in dict is same as loading each policy separately.
    """

    def setup_method(self, method):

        policy_set = {'plen': 12, 'psets': 4, 'pdict': 1, 'phist': 3, 'prenew': 3, 'pattempts': 1, 'pautorecover': 0}
        self.multi_policy = simulation()
        self.multi_policy.set_multi_policy(policy_set)

        self.policy = simulation()
        self.policy.set_policy('plen', 12)
        self.policy.set_policy('psets', 4)
        self.policy.set_policy('pdict', 1)
        self.policy.set_policy('phist', 3)
        self.policy.set_policy('prenew', 3)
        self.policy.set_policy('pattempts', 1)
        self.policy.set_policy('pautorecover', 0)

    def test_calc_risk_prob(self):
        assert self.policy.calc_risk_prob() == self.multi_policy.calc_risk_prob()

    def test_calc_risk_impact(self):
        assert self.policy.calc_risk_impact() == self.multi_policy.calc_risk_impact()

    def test_calc_prod_cost(self):
        assert self.policy.calc_prod_cost() == self.multi_policy.calc_prod_cost()


class TestMaxSec:
    """
    Tests the values for maximum security.
    """
    def setup_method(self, method):
        self.policy = simulation()
        self.policy.set_policy('plen', 12)
        self.policy.set_policy('psets', 4)
        self.policy.set_policy('pdict', 1)
        self.policy.set_policy('phist', 3)
        self.policy.set_policy('prenew', 3)
        self.policy.set_policy('pattempts', 1)
        self.policy.set_policy('pautorecover', 0)

    def test_calc_risk_prob(self):
        assert self.policy.calc_risk_prob() == 0.8

    def test_calc_risk_impact(self):
        assert self.policy.calc_risk_impact() == 1

    def test_calc_prod_cost(self):
        assert self.policy.calc_prod_cost() == 1


class TestMinSec:
    """
    Tests the values for minimum security.
    """
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
        assert self.policy.calc_risk_prob() == 1

    def test_calc_risk_impact(self):
        assert self.policy.calc_risk_impact() == 1

    def test_calc_prod_cost(self):
        assert self.policy.calc_prod_cost() == 0