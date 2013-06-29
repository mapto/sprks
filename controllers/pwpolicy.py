import web
import json
import environment
from sim.simulation import simulation
from datetime import timedelta, datetime
from environment import render_private as render
from environment import db
from models.pw_policy import pw_policy_model
from environment import get_start_time


class pwpolicy:
    # the default policy should be specified in a central place and reusable
    default = {"plen": 8, "psets": 2, "pdict": 0,
               "phist": 1, "prenew": 1, "pattempts": 0,
               "pautorecover": 1}

    def GET(self):
        """
        Renders the form to input password policies.
        """
        if environment.session.user_id > 0:
            #use this variable to request any ID number
            id_user = environment.session.user_id
            check = db.select('pw_policy', where="userid=$id_user", order="date DESC", vars=locals())
            if len(check) > 0:
                result_get = check[0]
                environment.session.date = result_get.date
                return render.pwpolicy_form(environment.session.user_id,result_get.userid, result_get.plen, result_get.psets,
                                result_get.pdict, result_get.phist, result_get.prenew,
                                result_get.pattempts, result_get.pautorecover, 0, str(result_get.date))
            else:
#                dt = datetime.now()
#                dtt = dt - timedelta(days=dt.weekday()) #goes back to last monday
                # The default policy (i.e. when not specified by user)
                dtt = get_start_time()
                db.insert('pw_policy', userid=id_user, date=dtt.strftime("%Y/%m/%d %H:%M:%S"),
                          plen=pwpolicy.default["plen"],
                          psets=pwpolicy.default["psets"],
                          pdict=pwpolicy.default["pdict"],
                          phist=pwpolicy.default["phist"],
                          prenew=pwpolicy.default["prenew"],
                          pattempts=pwpolicy.default["pattempts"],
                          pautorecover=pwpolicy.default["pautorecover"])
                result_get = db.select('pw_policy', where="userid=$id_user", vars=locals())[0]
                environment.session.date = result_get.date
                return render.pwpolicy_form(environment.session.user_id, result_get.userid, result_get.plen, result_get.psets,
                                result_get.pdict, result_get.phist, result_get.prenew,
                                result_get.pattempts, result_get.pautorecover, 1, result_get.date)
        else:
            raise web.seeother('/home')

    def POST(self):
        web.header('Content-Type', 'application/json')
        sim = simulation()
        payload = json.loads(web.data())
        data = eval(payload["data"])
        if "pdict" in data:
            dict1=1
        else:
            data["pdict"]=0
        if "pautorecover" in data:
            pautorecover1=1
        else:
            data["pautorecover"]=0
        if "pattempts" in data:
            pattempts1=1
        else:
            data["pattempts"]=0
        pw_policy_model().update({'userid':str(environment.session.user_id), 'date':payload["date"]}, data)
        for k, value in data.iteritems():
            sim.set_policy(k, value)
        return json.dumps([{"name": "prob", "value": sim.calc_risk_prob()},
                           {"name": "impact", "value": sim.calc_risk_impact()},
                           {"name": "cost", "value": sim.calc_prod_cost()}])
