__author__ = 'Horace'

import unittest
import dummy_class
from sim.simulation import policy_plen

class TestNumbers(unittest.TestCase):
    def test_one(self):
        codeTest = dummy_class.index()
        self.assertEqual(codeTest.func(3), 4)

class TestPolicy(unittest.TestCase):
    def test_plen_prob(self):
        policy_test = policy_plen(8)
        self.assertEqual(policy_test.get_risk_prob(8), .75)