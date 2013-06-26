__author__ = 'Horace'

from estimator_sklearn_tree import estimator_sklearn_tree
from estimator_simple import estimator_simple
from classifier_sklearn import classifier_sklearn


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
        risk = self.classifier.predict(self.dict)[0]
        # Extreme precision is not needed outside of simulation
        return round(risk, 2)

    def calc_risk_impact(self):
#        impact = self.estimator.get_risk_impact(self.dict)
        # Extreme precision is not needed outside of simulation
        return round(1, 2)

    def calc_prod_cost(self):
        #cost = self.estimator.get_prod_cost(self.dict)
        cost = self.classifier.predict(self.dict)[1]
        # Extreme precision is not needed outside of simulation
        return round(cost, 2)