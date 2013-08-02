from sim.model_sklearn import classifier_sklearn

"""
for policy specification see ranges variable in
https://github.com/mapto/sprks/blob/master/models/pw_policy.py and policies.py
"""


class simulation:
    def __init__(self):
        """
        Initialization of the simulation. This class always assumes that there's a policy being set.
        Before using it, make sure you update the policy with the one you want to use.
        TODO: This class does not take care of partial policies
        :param policies: A dictionary of policies being explicitly set
        """
        self.classifier = classifier_sklearn()

    #        self.estimator = estimator_simple()


    # OBSOLETE: use get_related_incidents instead as each policy determines one incident per risk
    def get_incident(self, policy):
        """ The public interface to get
        """
        risk = self.classifier.predict_data(policy)
        value = risk[0]  # 0 - name, 1 - risk
        return value


    def get_related_incidents(self, policy, context = {}):
        """
        Returns incidents for a particular policy. Accepts full policy (i.e smth like {"plen": 12, "psets": 1, "pdict": 1,
               "phist": 1, "prenew": 1, "pattempts": 2,
               "precovery": 1, "pdata": 0, "bdata": 1} )
        :param policy: policy
        """
        result = self.classifier.predict_data(policy, context)
        return result

if __name__ == "__main__":
    default = {"plen": 12, "psets": 1, "pdict": 1,
               "phist": 1, "prenew": 1, "pattempts": 2,
               "precovery": 1, "pdata": 0, "bdata": 1}
    sim = simulation()
    print sim.get_related_incidents(default)
