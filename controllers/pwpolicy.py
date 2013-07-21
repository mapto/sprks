"""
OBSOLETE
"""

import json
import web
import localsys
from sim.simulation import simulation
from localsys.storage import db
from localsys.storage import path
from localsys.environment import context
from models.pw_policy import pw_policy_model
from models.score import score_model
from localsys.environment import render

class pwpolicy:
    def GET(self):
        if context.user_id() == 0:
            raise web.seeother(path + '/home')
        return render.pwpolicy_form()

    # OBSOLETE
    # This seems to make simulation calls that are long outdated
    def POST(self):
        web.header('Content-Type', 'application/json')
        sim = simulation()
        msg = {}
        payload = json.loads(web.data())
        data = payload['data']

        pw_policy_model.update(
            {
                'userid': context.user_id(),
                'date': payload['date']
            }, data)

        calendar = calendar_model.get_calendar(data, payload['newCosts'], payload['date'])

        for k, value in data.iteritems():
            sim.set_policy(k, value)
        msg['msg1'] = [{'name': 'risk', 'value': sim.calc_risk_prob()},
                       {'name': 'cost', 'value': sim.calc_prod_cost()}]
        msgs = []
        tmp_msg = {}
        tmp_msg['id'] = payload['id']
        tmp_msg['data'] = data
        msgs.append(tmp_msg)
        my_list = ['plen', 'psets', 'pdict', 'phist', 'prenew', 'pattempts', 'precovery']
        for key in my_list:
            tmp_policy = pw_policy_model.get_range(data, key)
            for k in tmp_policy:
                msgs.append(k)
        scores = score_model().multiple_score(msgs)
        msg['msg2'] = scores
        msg['calendar'] = calendar
        return json.dumps(msg)


class pwpolicy_rest:

     # the default policy should be specified in a central place and reusable
    default = pw_policy_model.default.copy()
    #    default['date'] = get_start_time().isoformat()
    def GET(self):
        """
        Handles AJAX requests to get client's most recent policies.
        """

        if context.user_id() == 0:
            raise web.seeother(path + '/home')

        check = db.select('pw_policy', where='userid=$context.user_id()', order='date DESC', vars=locals())
        if len(check) > 0:
            result_get = check[0]
            return json.dumps(
                {
                    'plen': result_get.plen,
                    'psets': result_get.psets,
                    'pdict': result_get.pdict,
                    'phist': result_get.phist,
                    'prenew': result_get.prenew,
                    'pattempts': result_get.pattempts,
                    'precovery': result_get.precovery,
                    'date': result_get.date
                }
            )

        else:
            return json.dumps(self.default_policy)
