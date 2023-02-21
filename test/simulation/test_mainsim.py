
import glob
import json
import csv

from models.company import company
from models.policies import policies_model
from sim.train_sklearn import train_sklearn
from sim.model_sklearn import regression_sklearn
from sim.model_sklearn import classifier_sklearn

class TestGeneration:
    all_risks = ["bruteforce", "stolen"] # this needs to be derived from actual incident json files
    default_context = {
            'employees': company.employee_types,
            'locations': company.location_types,
            'devices': company.device_types}

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

    # def test_training_data(self):
    #     for next in self.entries:
    #         print(next)
    #         assert self.classifier.predict_data(next) == 'classifier'
    #         print(self.classifier.predict_data(next))

    def generate_testing_set(self):
        """
        Generalizes the incidents into a training set to be used by the implicit model.
        This assumes the types of risks
        """

        result = []

        # read incidents and generate training sets
        for ref in glob.glob('static/incidents/*.json'):
            incident_file = open(ref)
            incident = json.load(incident_file)
            incident_file.close()

            risks = self.all_risks if incident["type"] == 'general' else [incident["type"]]
            policy = incident["policy"]
            cls = incident["id"]
            value = incident["risk"]

            # fill missing part of context, assuming that omitting something means all possible values
            if "context" in incident:
                context = incident["context"]
                for key in self.default_context:
                    if key not in context:
                        context[key] = self.default_context[key]
            else:
                context = self.default_context

            # complete policy with neutral values
            sample = policies_model.get_neutral() # no need to copy, because call already returns a new instance
            sample.update(policy)

            # add classification last column
            data = policies_model.policy2datapoint(sample)

            self.trainer = train_sklearn()
            self.classifier = classifier_sklearn()
            self.regression = regression_sklearn()

            line = []
            line.append(incident["name"])
            line.append(incident["type"])
            line.append(cls)
            line.append(value)
            print(str(incident["name"]) + " policy: " + str(data) + " context: " + str(context) + " risks: " + str(risks))
            for risk in self.all_risks:
                for employee in context['employees']:
                    for location in context['locations']:
                        for device in context['devices']:
                            if risk in risks and employee in self.default_context['employees'] and location in self.default_context['locations'] and device in self.default_context['devices']:
                                # print risk + " " + employee + " " + location + " " + device
                                # print "classification: (" + str(cls) + "," + str(self.classifier.get_prediction(data, employee, location, device, risk)["id"]) + ")"
                                # print "regression: (" + str(value) + "," + str(self.regression.get_prediction(data, employee, location, device, risk)) + ")"
                                line.append(self.classifier.get_prediction(data, employee, location, device, risk)["id"])
                                line.append(self.regression.get_prediction(data, employee, location, device, risk))
                            else:
                                line.append(0)
                                line.append(0)
            result.append(line)

        writer = csv.writer(open('result.csv', 'wb'))
        label = ['name', 'risk', 'cls', 'prob']
        for risk in self.all_risks:
            for employee in context['employees']:
                for location in context['locations']:
                    for device in context['devices']:
                        label.append(risk + '-' + employee + '-' + location + '-' + device)
                        label.append(risk + '-' + employee + '-' + location + '-' + device)
        writer.writerow(label)
        writer.writerows(result)


if __name__ == "__main__":
    TestGeneration().generate_testing_set()