from __future__ import division # make division floating, not integer: http://stackoverflow.com/questions/1267869/how-can-i-force-division-to-be-floating-point-in-python

__author__ = 'Horace'

from estimator_sklearn_tree import estimator_sklearn_tree
from estimator_simple import estimator_simple
from classifier_sklearn import classifier_sklearn

"""
plen: {0, 6, 8, 10, 12} // value of the shortest permitted password
psets: {1, 2, 3, 4} // number of symbol sets that must be used
pdict: {1, 0}  // are passwords checked whether they match a dictionary
phist: {0, 1, 2, 3}  // history check of passwords resp. none, minimum (1 past password, exact match), strict (2 past passwords, string distance of 2), extreme (4 past passwords, string distance of 5)
prenew: {0, 1, 2, 3} // when the localsys asks users to renew passwords: never, annually, quarterly, monthly
pattempts: {1, 0} // is there a limit on wrong password attempts
pautorecover: {1, 0} // are forgotten passwords restored automatically(1), or is there human support(0)
"""


class simulation:
    def __init__(self, policies={}):
        if not hasattr(self, 'dict'):
        # lazy initialization of policies dictionary
            self.dict = {}
        self.set_multi_policy(policies)
        self.estimator = estimator_sklearn_tree()
        self.classifier = classifier_sklearn()

    #        self.estimator = estimator_simple()

    def set_multi_policy(self, policies):
        """
        Accept policy as dict.
        """
        for k, v in policies.iteritems():
            self.set_policy(k, v)

    def set_policy(self, policy_name, policy_value):
        """
        Sets a parameter to the user policy.

        Possible parameters are (for meanings check specific policy classes):
        plen: {0, 6, 8, 10, 12}
        psets: {1, 2, 3, 4}
        pdict: {1, 0}
        phist: {0, 1, 2, 3}
        prenew: {0, 1, 2, 3}
        pattempts: {1, 0}
        pautorecover: {1, 0}
        """

        # Risk probability and impact are multiplied together
        # Productivity costs are added together

        self.dict[policy_name] = self.load_policy(policy_name)(policy_value)

    def load_policy(self, policy_name):
        """
        If required policy class is already loaded, returns it.
        Otherwise imports the module and the class within.
        """

        policy_id = "policy_" + policy_name
        if policy_id in globals():
            return globals()[policy_id]
        else:
            """ The following code composes e.g. the following:

                    import sim.policy_plen
                    return_value = policy_len.policy_len()

                First one is module name (file), second one is class name
                Not only these two names coincide,
                but also class is attribute of module and constructor method (?policy_id?) is a attribute of class
            """
            # lazy class loading
            policy_module = __import__('sim.' + policy_id)
            # weird hack... no idea why we need getattr twice...
            return getattr(getattr(policy_module, policy_id), policy_id)

    def calc_risk_prob(self):
        #risk = self.estimator.get_risk_prob(self.dict)
        risk = self.classifier.predict_data(self.dict)
        value = risk[1]  # 0 - name, 1 - risk
        # Extreme precision is not needed outside of simulation
        return round(value, 2)

    def calc_risk_impact(self):
    #        impact = self.estimator.get_risk_impact(self.dict)
        # Extreme precision is not needed outside of simulation
        return 1
        # return round(1, 2)

    def derive_maintenance_cost(self, policy):
        # range for complexity [7, 48]
        complexity = policy["plen"].value()\
                   + policy["psets"].value() * 3\
                   + policy["pdict"].value() * 12\
                   + policy["phist"].value() * 4

        generation = complexity * policy["prenew"].value()  # range for generation [0, 144]
        memorization = generation + policy["pattempts"].value() * 24 # range [0, 192]
        support = (policy["pattempts"].value() * 24 + memorization) * policy["pautorecover"].value() # range [0, 240]

        return support / 240 # normalized, notice from _future_ import that converts division to floating. default is integer division

    def derive_prod_cost(self, policy):
        """ Productivity cost can be derived from a clear formula.
            There are other less obvious costs that need to be derived with machine learning algorithm.
            These are compliance cost and risk impact (not for passwords)
        """
        # range for complexity [7, 48]
        complexity = policy["plen"].value()\
                   + policy["psets"].value() * 3\
                   + policy["pdict"].value() * 12\
                   + policy["phist"].value() * 4

        generation = complexity * policy["prenew"].value() # range for generation [0, 144]
        gen_norm = generation / 144 # notice from _future_ import that converts division to floating. default is integer division

        memorization = generation + policy["pattempts"].value() * 24 # range [0, 192]
        mem_norm = memorization / 192

        entry = policy["plen"].value() # range [0, 12]
        entry_norm = entry / 12

        return (gen_norm + mem_norm + entry_norm) / 3

    def calc_prod_cost(self):
        """ To ensure consistency across system, keep values in the [0, 1] range
        """
        #cost = self.estimator.get_prod_cost(self.dict)
        # cost = self.classifier.predict(self.dict)[1]
        productivity = self.derive_prod_cost(self.dict)
        maintenance = self.derive_maintenance_cost(self.dict)

        cost = (productivity + maintenance) / 2 # overall (needs to be weighted) cost
        # Extreme precision is not needed outside of simulation
        return round(cost, 2)

    def get_incident(self):
        risk = self.classifier.predict_data(self.dict)
        value = risk[0]  # 0 - name, 1 - risk
