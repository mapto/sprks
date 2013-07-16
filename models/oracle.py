from models.journal import records
from sim.simulation import simulation
from localsys.storage import db
from models.incident import incident
from models.company import company
import random
from datetime import timedelta
from models.policies import policies_model


class prophet:
    @classmethod
    def prophesize(cls, user_id, base_date):
        """
        Given user_id, returns prophecy, a list of dictionaries of events.
        Events start from specified base_date, offset from 0 to 30 days.
        [
            {
                'date': 'YYYY-MM-DD'
                'incident_id': 1,
                'cost': 5000000
            },
            ...
        ]
        """

        random.seed()

        #policies = db.query('SELECT * FROM policies WHERE user_id=$user_id ORDER BY date DESC limit 1', vars=locals())
        policies = policies_model().nested_obj_to_list_of_dict(policies_model().iter_to_nested_obj(policies_model().get_policy_history(user_id, True)))[0]['data']
        incidents = simulation().get_related_incidents(policies)

        prophecy = []
        for incident_id in incidents:
            current_incident = incident.get_incident(incident_id)

            """
            Calling method on a dict?? am I missing something?
            """
            #daily_prob = cls.daily_prob(current_incident.get_risk())
            daily_prob = cls.daily_prob(current_incident['risk'])
            #incident_cost = current_incident.get_cost()*company.max_incident_cost
            incident_cost = current_incident['cost']*company.max_incident_cost

            for i in range(0, 31):
                if random.random() < daily_prob:
                    prophecy.append({
                        'date': (base_date + timedelta(days=i)).isoformat(),
                        'incident_id': incident_id,
                        'cost': cls.randomize_cost(incident_cost)
                    })

        return prophecy

    @classmethod
    def daily_prob(cls, monthly_prob):
        """
        Given monthly probability of one or more successes P(x>=1) assuming a binomial distribution over 30 days,
        calculates the daily probability of success.

        monthly_prob = P(x>=1) = 1 - P(x=0)
        P(x=0) = (1-p)^30
        """
        return 1 - (1-monthly_prob)**(1/30)

    @classmethod
    def randomize_cost(cls, cost):
        """
        Given a cost (monetary value), adds a factor of randomization (+/- 20%) to the value.
        """
        offset = (random.random() - 0.5) * 0.4
        return cost * (1 + offset)