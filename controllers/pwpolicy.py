import web
import json
import localsys
from sim.simulation import simulation
from localsys.environment import *
from localsys.storage import db
from models.pw_policy import pw_policy_model
from libraries.user_helper import auth


class pwpolicy:
    # the default policy should be specified in a central place and reusable
    default = {"plen": 8, "psets": 2, "pdict": 0,
               "phist": 1, "prenew": 1, "pattempts": 0,
               "pautorecover": 1}

    def GET(self):
        """
        Renders the form to input password policies.
        """
        user_id = auth().check()
        if user_id == 0:
            raise web.seeother('home')

        check = db.select('pw_policy', where="userid=$user_id", order="date DESC", vars=locals())
        if len(check) > 0:
            result_get = check[0]
            localsys.storage.session.date = result_get.date
            return render.pwpolicy_form(users_model().get_username(user_id), user_id, result_get.plen,
                                        result_get.psets,
                                        result_get.pdict, result_get.phist, result_get.prenew,
                                        result_get.pattempts, result_get.pautorecover, 0, str(result_get.date))
        else:
        #                dt = datetime.now()
        #                dtt = dt - timedelta(days=dt.weekday()) #goes back to last monday
            # The default policy (i.e. when not specified by user)
            dtt = get_start_time()
            db.insert('pw_policy', userid=user_id, date=dtt.strftime("%Y/%m/%d %H:%M:%S"),
                      plen=pwpolicy.default["plen"],
                      psets=pwpolicy.default["psets"],
                      pdict=pwpolicy.default["pdict"],
                      phist=pwpolicy.default["phist"],
                      prenew=pwpolicy.default["prenew"],
                      pattempts=pwpolicy.default["pattempts"],
                      pautorecover=pwpolicy.default["pautorecover"])
            result_get = db.select('pw_policy', where="userid=$user_id", vars=locals())[0]
            localsys.storage.session.date = result_get.date
            return render.pwpolicy_form(users_model().get_username(user_id), user_id, result_get.plen,
                                        result_get.psets,
                                        result_get.pdict, result_get.phist, result_get.prenew,
                                        result_get.pattempts, result_get.pautorecover, 1, result_get.date)

    def POST(self):
        web.header('Content-Type', 'application/json')
        sim = simulation()
        payload = json.loads(web.data())
        data = eval(payload["data"])
        if "pdict" not in data:
            data["pdict"] = 0
        if "pautorecover" not in data:
            data["pautorecover"] = 0
        if "pattempts" not in data:
            data["pattempts"] = 0
        pw_policy_model().update({'userid': str(localsys.session.user_id), 'date': payload["date"]}, data)
        for k, value in data.iteritems():
            sim.set_policy(k, value)
#        return json.dumps(data)
        return json.dumps([{"name": "risk", "value": sim.calc_risk_prob()},
                           {"name": "cost", "value": sim.calc_prod_cost()}])
