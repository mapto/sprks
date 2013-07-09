import json
import web
import localsys
from sim.simulation import simulation
from localsys.environment import *
from localsys.storage import db
from models.pw_policy import pw_policy_model
import string
from models.score import score_model
from models.calendar import calendar_model


class pwpolicy:
    def GET(self):
        user_id = context.user_id()
        if user_id == 0:
            raise web.seeother('home')
        return render.pwpolicy_form()

    def POST(self):
        web.header('Content-Type', 'application/json')
        sim = simulation()
        msg = {}
        payload = json.loads(web.data())
        data = eval(payload['data'])
        if 'pdict' not in data:
            data['pdict'] = 0
        if 'precovery' not in data:
            data['precovery'] = 0
        if 'pattempts' not in data:
            data['pattempts'] = 0

        pw_policy_model().update({'userid': context.user_id(), 'date': payload['date']}, data)

        #get the calendar
        calendar = calendar_model().get_calendar(data=data, cost=payload['recent_cost'], date=payload['date'])

        for k, value in data.iteritems():
            sim.set_policy(k, value)
#        return json.dumps(data)
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
        print 'final data'
        print msgs
        scores = score_model().multiple_score(msgs)
        msg['msg2'] = scores
        msg['calendar'] = calendar
        return json.dumps(msg)


class pwpolicy_rest:

    default_policy = {
        'plen': 8,
        'psets': 2,
        'pdict': 0,
        'phist': 1,
        'prenew': 1,
        'pattempts': 0,
        'precovery': 1,
        'date': get_start_time().isoformat()
    }

    def GET(self):
        """
        Handles AJAX requests to get client's most recent policies.
        """

        if context.user_id() == 0:
            raise web.seeother('home')

        check = db.select('pw_policy', where='userid=$context.user_id()', order='date DESC', vars=locals())
        if len(check) > 0:
            result_get = check[0]
            localsys.storage.session.date = result_get.date

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
