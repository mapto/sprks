__author__ = 'Horace'

import sim
from sim.policy_plen import policy_plen


class TestPLen:
    def test_plen_prob(self):
        policy_test = sim.policy_plen.policy_plen(8)
        assert policy_test.get_risk_prob() == .75