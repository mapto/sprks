__author__ = 'Horace'

import sim


class TestPLen:
    def test_plen_prob(self):
        policy_test = sim.policy_plen.policy_plen(8)
        assert policy_test.get_risk_prob() == .75