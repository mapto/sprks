__author__ = 'zhanelya'

from localsys.environment import context
from localsys.environment import render
from localsys.storage import path
from models.score import score_model
from models.policies import policies_model
import json
import web
from sim.simulation import simulation


class score:
    def GET(self):
        #check if is logged in
        if context.user_id() > 0:
            return render.score()
        #previously rendered with: context.username(),localsys.storage.session.date and scores from get_scores
        else:
            #if user not logged in -> redirect to login page
            raise web.seeother(path + '/home')


class score_rest:
    def GET(self):
        return json.dumps(score_model.get_scores(context.user_id()))


# This seems to make simulation calls that are long outdated
# However, it is not obsolete, because the multiple scores functionality is needed
class multiple_score:
    def POST(self):
        web.header('Content-Type', 'application/json')
        sim = simulation()
        post_data = json.loads(web.data())
        policy_costs_risks = []

        last_policy = policies_model().get_policy_history(context.user_id())
        for policy_entry in post_data:
            result_entry = {}
            for key, value in policy_entry.iteritems():
                if key == "data":
                    next_policy = json.loads(value)
                else:
                    result_entry[key] = value
            result_entry["risk"] = sim.calc_risk_prob(next_policy)
            result_entry["cost"] = sim.calc_prod_cost(next_policy)
            policy_costs_risks.append(result_entry)

        # print('return cost '+ policy_costs_risks)

        return json.dumps(policy_costs_risks)
