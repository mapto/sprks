from sim.simulation import *
import numpy
from numpy import genfromtxt
from models.policies import policies_model
from sim.train_sklearn import train_sklearn


class TestGeneration:
    """
    Tests the creation of permutations for the needs of training of implicit model
    """
    def test_enumerations(self):
        assert len(train_sklearn().enum_policy_contexts()) == 27
        product = 1
        for next in policies_model.get_ranges():
            product = product * len(policies_model.get_ranges()[next])

        assert len(train_sklearn().enum_samples({})) == product