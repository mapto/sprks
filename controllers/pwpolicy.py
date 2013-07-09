import json
from json import JSONEncoder
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
        data = eval(payload["data"])
        if "pdict" not in data:
            data["pdict"] = 0
        if "precovery" not in data:
            data["precovery"] = 0
        if "pattempts" not in data:
            data["pattempts"] = 0

        pw_policy_model().update({'userid': context.user_id(), 'date': payload["date"]}, data)

        #get the calendar
        calendar = calendar_model().get_calendar(data=data, cost=payload["recent_cost"], date=payload["date"])

        for k, value in data.iteritems():
            sim.set_policy(k, value)
#        return json.dumps(data)
        msg["msg1"] = [{"name": "risk", "value": sim.calc_risk_prob()},
                       {"name": "cost", "value": sim.calc_prod_cost()}]
        msgs = []
        tmp_msg = {}
        tmp_msg["id"] = payload["id"]
        tmp_msg["data"] = data
        msgs.append(tmp_msg)

        my_list = ["plen", "psets", "pdict", "phist", "prenew", "pattempts", "precovery"]
        for key in my_list:
            tmp_policy = pw_policy_model.get_range(data, key)
            for k in tmp_policy:
                msgs.append(k)
        print "final data"
        print msgs
        scores = score_model().multiple_score(msgs)
        msg["msg2"] = scores
        msg["calendar"] = calendar
        return json.dumps(msg)


class pwpolicy_rest:
     # the default policy should be specified in a central place and reusable
    default = {"plen": 8, "psets": 2, "pdict": 0,
               "phist": 1, "prenew": 1, "pattempts": 0,
               "precovery": 1}

    def GET(self):
        """
        Renders the form to input password policies.
        """
        user_id = context.user_id()
        if user_id == 0:
            raise web.seeother('home')

        check = db.select('pw_policy', where="userid=$user_id", order="date DESC", vars=locals())
        if len(check) > 0:
            result_get = check[0]
            localsys.storage.session.date = result_get.date

            json = JSONEncoder().encode({
                "plen": result_get.plen,
                "psets": result_get.psets,
                "pdict": result_get.pdict,
                "phist": result_get.phist,
                "prenew": result_get.prenew,
                "pattempts": result_get.pattempts,
                "precovery": result_get.precovery,
                "notfound": 0,
                "date": str(result_get.date)[0:string.find(str(result_get.date), ' ')]
                })

        else:
            # The default policy (i.e. when not specified by user)
            dtt = get_start_time()
            string_time = dtt.strftime("%Y/%m/%d")
            localsys.storage.session.date = string_time

            json = JSONEncoder().encode({
                "plen": self.default["plen"],
                "psets": self.default["psets"],
                "pdict": self.default["pdict"],
                "phist": self.default["phist"],
                "prenew": self.default["prenew"],
                "pattempts": self.default["pattempts"],
                "precovery": self.default["precovery"],
                "notfound": 1,
                "date": string_time
                })

        return json

