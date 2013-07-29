__author__ = 'Daniyar'

from sklearn import svm
import cPickle
import numpy
from models.company import company
from models.incident import incident
from models.policies import policies_model as policy_model


class classifier_sklearn:
    risks_set = ["bruteforce", "stolen"] # this needs to be derived from actual incident json files

    def __init__(self):
        """
        Initializes all implicit models.
        Currently there is one model per risk,
        but should turn into one model per risk per environmental configuration
        :param user_id:
        :param sync_date:
        """
        self.incidents_models = {}
        self.risks = []
        check_classifier = True
        f = open('static/data/classifier-models.txt','rb')
        self.incidents_models = cPickle.load(f)
        f.close()

    def predict_data(self, data, context = {}):
        """
        Makes a prediction for a particular policy
        Currently only handles pw_policy, but in future data preparation needs to be handled by the model.
        :param data: The policy configuration that needs to be consistent with the used data structure
        """
        datapoints = policy_model.policy2datapoint(data)
        result = self.predict_datapoint(datapoints, context)
        return result

    def predict_datapoint(self, datapoints, p_context = {}, risks = risks_set):
        """
        Makes a prediction for a particular policy datapoint, given all implicit models
        For external use, please refer to predict_data
        :param datapoint: The data as a tuple
        :param p_context: A dictionary representing (possibly multiple) environmental context of the policy
        """
        context = dict(p_context) # clones the list, so that the parameter doesn't get modified
        if 'employees' not in context:
            context['employees'] = company.employee_types
        elif len(context['employees']) == 0:
            context['employees'] = company.employee_types
        if 'locations' not in context:
            context['locations'] = company.location_types
        elif len(context['locations']) == 0:
            context['locations'] = company.location_types
        if 'devices' not in context:
            context['devices'] = company.device_types
        elif len(context['devices']) == 0:
            context['devices'] = company.device_types

        risks_list = []
        tmp_list = {}

        # Iterates through classifier models to estimate class for different locations, workers and devices
        # Returns list of incidents
        for next_risk in risks:
            my_list = []
            for employee in context['employees']:
                for location in context['locations']:
                    for device in context['devices']:
                        models = self.incidents_models
                        response = self.incidents_models[next_risk][employee][location][device].predict(datapoints)
                        # Algorithm returns list of predictions.
                        # Because of the dataset it contains only one element
                        # data is returned as an array of numpy.float64, we need integers so we could use them as incident indices
                        # event = incident(cls[0].astype(int64))
                        # risk = event.get_risk()
                        event = incident.get_incident(cls)
                        my_list.append(event)
                        #risks_list.append(event["id"])
            tmp_list[next_risk] = my_list

        # Finds the incident with maximum risk probability per risk
        for next_risk in tmp_list: # for each risk type
            max = incident.get_most_probable(tmp_list[next_risk])
            risks_list.append(max)

        return risks_list
        #return self.incidents_model.predict(data)

    def predict_single_datapoint(self, datapoints, context, risks = risks_set):
        """
        The difference to predict_datapoint is that only one context is being handled here

        :param datapoint: The data as a tuple
        :param p_context: The single environmental context of the policy,
                        make sure that it is a list featuring employee, location, device in that order
        """
        incidents_list = []

        # Iterates through classifier models to estimate class for different locations, workers and devices
        # Returns list of incidents
        for next_risk in risks:
            my_list = []
            response = self.incidents_models[next_risk][context['employee']][context['location']][context['device']].predict(datapoints)
            # Model returns an array. For our problem it happens to have only one element
            incidents_list.append(incident.get_incident(response[0]))

        max = incident.get_most_probable(incidents_list)

        return max
        #return self.incidents_model.predict(data)

if __name__ == "__main__":
    # result = model.generate_samples({'prenew': 3, 'pattempts': 3, 'pdict': 0, 'psets': 2, 'phist': 4})
    # result = model.generate_samples({'plen': 0})
    # result = model.generate_samples({})

    #test_data = [0,0,0,4,0,1,3,1,0]
    #test_data = policy_model.get_default()
    #model = classifier_sklearn()

    #print "test data: "
    #print test_data
    #print policy_model.policy2datapoint(test_data)
    #print "classes:"
    #print model.predict_datapoint(test_data)
    pass
