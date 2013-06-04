__author__ = 'Horace'


from sim.simulation import *


class TestPLen:
    def test_plen_prob(self):
        policy_test = policy_plen(8)
        assert policy_test.get_risk_prob() == .75