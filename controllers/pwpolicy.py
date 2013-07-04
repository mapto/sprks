import json
import web
import localsys
from sim.simulation import simulation
from localsys.environment import *
from localsys.storage import db
from models.pw_policy import pw_policy_model
from models.journal import records
import string


class pwpolicy:
    # the default policy should be specified in a central place and reusable
    default = {"plen": 8, "psets": 2, "pdict": 0,
               "phist": 1, "prenew": 1, "pattempts": 0,
               "pautorecover": 1}

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
            return render.pwpolicy_form(users_model.get_username(user_id), user_id, result_get.plen,
                                        result_get.psets,
                                        result_get.pdict, result_get.phist, result_get.prenew,
                                        result_get.pattempts, result_get.pautorecover, 0, str(result_get.date)[0:string.find(str(result_get.date), ' ')])
        else:
        #                dt = datetime.now()
        #                dtt = dt - timedelta(days=dt.weekday()) #goes back to last monday
            # The default policy (i.e. when not specified by user)
            dtt = get_start_time()
            string_time = dtt.strftime("%Y/%m/%d")
            db.insert('pw_policy', userid=user_id, date=string_time,
                      plen=pwpolicy.default["plen"],
                      psets=pwpolicy.default["psets"],
                      pdict=pwpolicy.default["pdict"],
                      phist=pwpolicy.default["phist"],
                      prenew=pwpolicy.default["prenew"],
                      pattempts=pwpolicy.default["pattempts"],
                      pautorecover=pwpolicy.default["pautorecover"])
            #result_get = db.select('pw_policy', where="userid=$user_id", vars=locals())[0]
            localsys.storage.session.date = string_time
            return render.pwpolicy_form(users_model().get_username(user_id), user_id, self.default["plen"],
                                        self.default["psets"],
                                        self.default["pdict"],self.default["phist"], self.default["prenew"],
                                        self.default["pattempts"], self.default["pautorecover"], 1, string_time)

    def POST(self):
        web.header('Content-Type', 'application/json')
        sim = simulation()
        msg = {}
        payload = json.loads(web.data())
        data = eval(payload["data"])
        if "pdict" not in data:
            data["pdict"] = 0
        if "precovery" not in data:
            data["pautorecover"] = 0
        if "pattempts" not in data:
            data["pattempts"] = 0
        pw_policy_model().update({'userid': context.user_id(), 'date': payload["date"]}, data)

        #get the calendar
        calendar = self.get_calendar(data=data, cost=payload["recent_cost"], date=payload["date"])

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

        my_list = ["plen", "psets", "pdict", "phist", "prenew", "pattempts", "pautorecover"]
        for key in my_list:
            tmp_policy = self.get_range(data, key)
            for k in tmp_policy:
                msgs.append(k)
        print "final data"
        print msgs
        scores = self.multiple_score(msgs)
        msg["msg2"] = scores
        msg["calendar"] = calendar
        return json.dumps(msg)

    def create_variation(self, policy, id, value):
        new_policy = {}
        for key in policy:
            new_policy[key] = policy[key]
        new_policy[id] = value
        return new_policy

    def get_range(self, policy, id):
        msgs = []
        sets = pw_policy_model.ranges
        for value in sets[id]:
            new_policy = self.create_variation(policy, id, value)
            msg = {}
            msg['id'] = id+str(value)
            msg["data"] = new_policy
            msgs.append(msg)

        return msgs

    def multiple_score(self, policies):
        post_data = policies
        policy_costs_risks = []
        sim = simulation()
        for policy_entry in post_data:
            result_entry = {}
            for key in policy_entry:
                if key == "data":
                    tmp_value = policy_entry[key]
                    sim.set_multi_policy(tmp_value)
                    result_entry["risk"] = sim.calc_risk_prob()
                    result_entry["cost"] = sim.calc_prod_cost()
                else:
                    result_entry["id"] = policy_entry[key]
            policy_costs_risks.append(result_entry)

            # print('return cost '+ policy_costs_risks)

        return policy_costs_risks

    def get_calendar(self, data, cost, date):
        web.header('Content-Type', 'application/json')
        usrid = context.user_id()
        sim = simulation()
        post_data = data
        policy = post_data

        for k, value in policy.iteritems():
            sim.set_policy(k, value)

        validation = records().validateJournal(cost, date, usrid) #0-if validation failed, 1-otherwise

        risk = sim.calc_risk_prob()
        cost = sim.calc_prod_cost()

        calendar = records().updateJournal(risk, usrid) #inserts new events into journal

        # TODO put this into model
       # dtt = datetime.strptime(date, "%Y/%m/%d")
       # string_time = dtt.strftime("%Y/%m/%d")
        db.insert('scores', userid=usrid, score_type=1, score_value=risk,
                  date=date, rank=0)
        db.insert('scores', userid=usrid, score_type=2, score_value=cost,
                  date=date, rank=0)
        db.insert('pw_policy', userid=usrid, date=date,
                  plen=data["plen"], psets=data["psets"], pdict=data["pdict"], phist=data["phist"],
                  prenew=data["prenew"], pattempts=data["pattempts"], pautorecover=data["pautorecover"])
       # return json.dumps([{"value": new_date.strftime("%Y/%m/%d %H:%M:%S")}])
        return calendar

