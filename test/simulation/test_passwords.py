__author__ = 'Horace'

import unittest
from sim.simulation import *


class TestPLen(unittest.TestCase):
    def test_plen_prob(self):
        policy_test = policy_plen(8)
        self.assertEqual(policy_test.get_risk_prob(), .75)