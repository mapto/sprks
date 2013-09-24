from models.simulation import simulation as sim_model
from models.company import company
import random
from datetime import timedelta
from models.policies import policies_model
from models.score import score_model


class prophet:
    @classmethod
    def prophesize(cls, user_id, base_date):
        """
        Given user_id, returns prophecy, a list of dictionaries of events.
        Events start from specified base_date, offset from 0 to 30 days.
        [
            {
        :param user_id:
        :param base_date:
                'date': 'YYYY-MM-DD'
                'incident_id': 1,
                'cost': 5000000
            },
            ...
        ]
        """

        random.seed()

        # policies = db.query('SELECT * FROM policies WHERE user_id=$user_id ORDER BY date DESC limit 1', vars=locals())
        # TODO lasagna code - this should be fixed when multiple policies are used.
        history = policies_model().get_policy_history(user_id, True)
        response = policies_model().nested_obj_to_list_of_dict(policies_model().iter_to_nested_obj(history))

        #Taking to consideration policy context for events prediction
        prophecy = []
        max_risk = 0
        max_cost = 0
        for policy in response:
            p = policy['data']
            p_context = {'employees': [p['employee']], 'locations': [p['location']], 'devices': [p['device']]}
            p_incidents = sim_model().request(p, p_context)
            for current_incident in p_incidents:
                if current_incident['risk'] > max_risk:
                    max_risk = current_incident['risk']
                    max_cost = current_incident['cost']
                daily_prob = cls.daily_prob(current_incident['risk'])
                incident_cost = current_incident['cost'] * company.max_incident_cost
                for i in range(0, 31):
                    rand = random.random()
                    if rand < daily_prob:
                        if len(prophecy) > 0:
                            for event in prophecy:
                                #check if one incident per day is generated (date is different for each event)
                                if ((base_date + timedelta(days=i)).isoformat()) == event['date']:
                                    break
                                else:
                                    #check if there are no duplicate incidents in prophecy
                                    if current_incident['id'] == event['incident_id']\
                                            and current_incident['employee'] == event['employee']\
                                            and current_incident['location'] == event['location']\
                                            and current_incident['device'] == event['device']:
                                        break
                                    else:
                                        if (prophecy.index(event)+1) == len(prophecy):
                                            prophecy.append({
                                                'date': (base_date + timedelta(days=i)).isoformat(),
                                                'incident_id': current_incident['id'],
                                                'cost': cls.randomize_cost(incident_cost),
                                                'employee': current_incident['employee'],
                                                'location': current_incident['location'],
                                                'device': current_incident['device']
                                            })
                        else:
                            prophecy.append({
                                'date': (base_date + timedelta(days=i)).isoformat(),
                                'incident_id': current_incident['id'],
                                'cost': cls.randomize_cost(incident_cost),
                                'employee': current_incident['employee'],
                                'location': current_incident['location'],
                                'device': current_incident['device']
                            })
        # TODO currently productivity costs is being used as risk impact.
        score_model.insert_score(user_id, 1, (max_risk * 4 + max_cost) / 5.0, base_date)
        score_model.insert_score(user_id, 2, (max_cost * 4 + max_risk) / 5.0, base_date)
        return prophecy

    @classmethod
    def daily_prob(cls, monthly_prob):
        """
        Given monthly probability of one or more successes P(x>=1) assuming a binomial distribution over 30 days,
        calculates the daily probability of success.

        monthly_prob = P(x>=1) = 1 - P(x=0)
        P(x=0) = (1-p)^30
        """
        return 1 - (1 - monthly_prob) ** (1.0 / 30)

    @classmethod
    def randomize_cost(cls, cost):
        """
        Given a cost (monetary value), adds a factor of randomization (+/- 20%) to the value.
        """
        offset = (random.random() - 0.5) * 0.4
        return cost * (1 + offset)


