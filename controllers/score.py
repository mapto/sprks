__author__ = 'zhanelya'

from localsys.environment import context
from localsys.environment import render
from models.score import score_model
import json
import web
from sim.simulation import simulation


class score:
    def GET(self):
        if context.user_id() > 0:
            return render.score()
        else:
            raise web.seeother('/home')


class score_rest:
    def GET(self):
        return json.dumps(score_model.get_scores(context.user_id()))


class multiple_score:
    def POST(self):
        web.header('Content-Type', 'application/json')
        sim = simulation()
        post_data = json.loads(web.data())
        policy_costs_risks = []
        for policy_entry in post_data:
            result_entry = {}
            for key, value in policy_entry.iteritems():
                if key == "data":
                    tmp_value = eval(value)
                    sim.set_multi_policy(tmp_value)
                    result_entry["risk"] = sim.calc_risk_prob()
                    result_entry["cost"] = sim.calc_prod_cost()
                else:
                    result_entry[key] = value
            policy_costs_risks.append(result_entry)

            # print('return cost '+ policy_costs_risks)

        return json.dumps(policy_costs_risks)

