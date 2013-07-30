__author__ = 'mruskov'

from localsys.storage import db
from models.policies import policies_model
from models.incident import incident
from sim.classifier_sklearn import classifier_sklearn
from models.company import company

class simulation:
    ordered_context = ['employee', 'location', 'device'] # has same elements as context, but is ordered the same way as database
    ordered_policy = ['bdata', 'pdata', 'plen', 'psets', 'pdict', 'phist', 'prenew', 'pattempts', 'precovery']

    def __init__(self):
        self.predictor = classifier_sklearn()

    def get(self, policy, context, risk):
        query = "SELECT `name` FROM `risks` WHERE"
        query = query + "`risk_type` = '" + risk + "'"
        for next in simulation.ordered_context:
            query = query + " AND `" + next + "` = '" + context[next] + "'"
        for next in simulation.ordered_policy:
            query = query + " AND `" + next + "` = " + str(policy[next])
        query = query + " LIMIT 1"
        return db.query(query)

    def set(self, policy, context, risk, name, value):
        if len(self.get(policy, context, risk)) > 0:
            raise Exception('Policy already exists in database')
        query = "INSERT INTO `risks` VALUES ('" + risk + "'"
        for next in simulation.ordered_context:
            query = query + ", '" + context[next] + "'"
        for next in simulation.ordered_policy:
            query = query + ", '" + str(policy[next]) + "'"
        query = query + ", '" + name + "', '" + str(value) + "')"
        return db.query(query)

    def update(self, policy, context, risk):
        if context['employee'] is None or context['location'] is None or context['device'] is None:
            raise KeyError('Expecting single context combination')

        response = self.get(policy, context, risk)

        if len(response) == 0:
            datapoint = policies_model.policy2datapoint(policy)
            result = self.predictor.predict_single_datapoint(datapoint, context, [risk])
            self.set(policy, context, risk, result['name'], result['risk'])
        else:
            result = incident.get_incident_by_name(response[0].name)

        return result


    def request(self, policy, p_context = {}, risk = 'any'):
        """
         Typical use of this would be
         :param risk: the risk that the policy is being examined against.
        """
        context = p_context.copy()
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

        risks = classifier_sklearn.risks_set if risk == 'any' else [risk]

        # Iterates through classifier models to estimate class for different locations, workers and devices
        # Returns list of incidents
        incidents = {}
        for next_risk in risks:
            my_list = []
            for employee in context['employees']:
                for location in context['locations']:
                    for device in context['devices']:
                        single_context = {'employee': employee, 'location': location, 'device': device}
                        response = self.update(policy, single_context, next_risk)
                        my_list.append(response)
                        #risks_list.append(event["id"])
            incidents[next_risk] = my_list

        # Finds the incident with maximum risk probability per risk
        result = []
        for next_risk in incidents: # for each risk type
            max = incident.get_most_probable(incidents[next_risk])
            result.append(max)

        return result


if __name__ == "__main__":
    a_context = {'employees': ['executives'], 'locations': ['office'], 'devices': ['phone']}
    policy = policies_model.get_default()
    print a_context
    print policy
    print simulation().request(policy, a_context)