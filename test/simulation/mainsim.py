__author__ = 'Horace'

import unittest
from sim.simulation import *


class TestSim(unittest.TestCase):

    def test_calc_risk_prob(self):
        policy = simulation()
        policy.set_policy('plen', 8)
        policy.set_policy('psets', 3)
        self.assertEqual(policy.calc_risk_prob(),0.375)

    def test_calc_prod_cost(self):
        policy = simulation()
        policy.set_policy('plen', 8)
        policy.set_policy('psets', 3)
        self.assertEqual(policy.calc_prod_cost(),7)

class TestPolicy(unittest.TestCase):
    def test_plen_prob(self):
        policy_test = policy_plen(8)
        self.assertEqual(policy_test.get_risk_prob(), .75)