
from models.policies import policies_model
from sim.train_sklearn import train_sklearn
from sim.model_sklearn import regression_sklearn
from sim.model_sklearn import classifier_sklearn

class TestGeneration:
    entries = [{
        "pdata": 0,
        "bdata": 0,
        "plen": 8,
        "psets": 1,
        "pdict": 1,
        "phist": 2,
        "prenew": 2,
        "pattempts": 0,
        "precovery": 0
    }]

    def setup_method(self, method):
        self.trainer = train_sklearn()
        self.classifier = classifier_sklearn()
        self.regression = regression_sklearn()

    """
    Tests the creation of permutations for the needs of training of implicit model
    """
    def test_enumerations(self):
        assert len(self.trainer.enum_policy_contexts()) == 27
        product = 1
        for next in policies_model.get_bounds():
            product = product * len(policies_model.get_bounds()[next])

        assert len(self.trainer.enum_samples({})) == product

    def test_training_data(self):
        for next in self.entries:
            print next
            assert self.classifier.predict_data(next) == 'classifier'
            print self.classifier.predict_data(next)
