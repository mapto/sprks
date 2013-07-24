from __future__ import division # make division floating, not integer: http://stackoverflow.com/questions/1267869/how-can-i-force-division-to-be-floating-point-in-python

from estimator_sklearn_tree import estimator_sklearn_tree
from classifier_sklearn import classifier_sklearn
from models.incident import incident

"""
for policy specification see ranges variable in https://github.com/mapto/sprks/blob/master/models/pw_policy.py
"""


class simulation:
    def __init__(self):
        """
        Initialization of the simulation. This class always assumes that there's a policy being set.
        Before using it, make sure you update the policy with the one you want to use.
        TODO: This class does not take care of partial policies
        :param policies: A dictionary of policies being explicitly set
        """
        self.classifier = classifier_sklearn("classifier")
        self.estimator = classifier_sklearn("estimator")


    def calc_risk_prob(self, policy):
        """ Returns the risk probability for this policy
            Notice that there are actually two different machine learning algotithms
            Incidents are identified with classification and risks are calculated with regression
        """
        return self.estimator.predict_data(policy)

    def calc_risk_impact(self):
        # impact = self.estimator.get_risk_impact(self.dict)
        # Extreme precision is not needed outside of simulation
        return 1
        # return round(1, 2)

    def derive_maintenance_cost(self, policy):
        # range for complexity [7, 48]
        complexity = int(policy["plen"])\
                   + int(policy["psets"]) * 3\
                   + int(policy["pdict"]) * 12\
                   + int(policy["phist"]) * 4

        generation = complexity * int(policy["prenew"])  # range for generation [0, 144]
        memorization = generation + int(policy["pattempts"]) * 24 # range [0, 192]
        support = (int(policy["pattempts"]) * 24 + memorization) * int(policy["precovery"]) # range [0, 240]

        return support / 240.0 # normalized, notice from _future_ import that converts division to floating. default is integer division

    def derive_prod_cost(self, policy):
        """ Productivity cost can be derived from a clear formula - this is an explicit model
            There are other less obvious costs that need to be derived with machine learning algorithm.
            These are compliance cost and risk impact (not for passwords)
        """
        # range for complexity [7, 48]
        complexity = int(policy["plen"])\
                   + int(policy["psets"]) * 3\
                   + int(policy["pdict"]) * 12\
                   + int(policy["phist"]) * 4

        generation = complexity * int(policy["prenew"]) # range for generation [0, 144]
        gen_norm = generation / 144.0 # notice from _future_ import that converts division to floating. default is integer division

        memorization = generation + int(policy["pattempts"]) * 24 # range [0, 192]
        mem_norm = memorization / 192.0

        entry = int(policy["plen"]) # range [0, 12]
        entry_norm = entry / 12.0

        return (gen_norm + mem_norm + entry_norm) / 3.0

    def calc_prod_cost(self, policy):
        """ To ensure consistency across system, keep values in the [0, 1] range
            This is the (explicit) model for productivity cost estimation
        """
        #cost = self.estimator.get_prod_cost(self.dict)
        # cost = self.classifier.predict(self.dict)[1]
        productivity = self.derive_prod_cost(policy)
        maintenance = self.derive_maintenance_cost(policy)

        cost = (productivity + maintenance) / 2.0 # overall (needs to be weighted) cost
        # Extreme precision is not needed outside of simulation
        return round(cost, 2)

    def get_incident(self, policy):
        """ The public interface to get
        """
        risk = self.classifier.predict_data(policy)
        value = risk[0]  # 0 - name, 1 - risk
        return value


    def get_related_incidents(self, policy):
        """
        Returns incidents for a particular policy. Accepts full policy (i.e smth like {"plen": 12, "psets": 1, "pdict": 1,
               "phist": 1, "prenew": 1, "pattempts": 2,
               "precovery": 1, "pdata": 0, "bdata": 1} )
        :param policy: policy
        """
        return self.classifier.predict_data(policy)

if __name__ == "__main__":
    default = {"plen": 12, "psets": 1, "pdict": 1,
               "phist": 1, "prenew": 1, "pattempts": 2,
               "precovery": 1, "pdata": 0, "bdata": 1}
    sim = simulation()
    print sim.get_related_incidents(default)
