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

    def calc_risk_prob(self, policy, p_context = {}, risk = 'any'):
        """
            Calculate the probability for the provided combination of policy, context and risk
            A typical call might omit context or risk,
            which would lead this method to assume that the request is for all possible combinations
        """
        #risk = self.estimator.get_risk_prob(self.dict)
        response = self.request(policy, p_context, risk)

        max = incident.get_most_probable(response)
        value = max['risk']
        # Extreme precision is not needed outside of simulation
        return round(value, 2)

    def calc_risk_impact(self):
    #        impact = self.estimator.get_risk_impact(self.dict)
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

    def calc_prod_cost(self, policy, p_context = {}):
        """ To ensure consistency across system, keep values in the [0, 1] range
            The current calculation ignores context
            Unlike risk probability, productivity cost depends on the policies (for each context) only
            and is not related to a particular risk.
        """
        #cost = self.estimator.get_prod_cost(self.dict)
        # cost = self.classifier.predict(self.dict)[1]
        productivity = self.derive_prod_cost(policy)
        maintenance = self.derive_maintenance_cost(policy)

        cost = (productivity + maintenance) / 2.0 # overall (needs to be weighted) cost
        # Extreme precision is not needed outside of simulation
        return round(cost, 2)


if __name__ == "__main__":
    a_context = {'employees': ['executives'], 'locations': ['office'], 'devices': ['phone']}
    policy = policies_model.get_default()
    print a_context
    print policy
    print simulation().request(policy, a_context)