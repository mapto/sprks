import web
import json
import session
from sim.simulation import simulation
from datetime import time, timedelta, datetime, date
from environment import render_private as render
from environment import db
from models.pw_policy import pw_policy_model

class pwpolicy_form:
    # the default policy should be specified in a central place and reusable
    default = {"plen": 8, "psets": 2, "pdict": 0,
               "phist": 1, "prenew": 1, "pattempts": 0,
               "pautorecover": 1}

    def GET(self):
        if session.mysession.session.loggedin:
            #use this variable to request any ID number
            id_user = session.mysession.session.id
            check = db.select('pw_policy', where="userid=$id_user", order="date DESC", vars=locals())
            if len(check) > 0:
                notfound=0
              #  result_get = db.select('pw_policy', where="idpolicy=$id_tmp", vars=locals())[0]
                result_get = check[0]
                session.mysession.session.date = result_get.date
                return render.pwpolicy_form(session.mysession.session.user,result_get.userid, result_get.plen, result_get.psets,
                                result_get.pdict, result_get.phist, result_get.prenew,
                                result_get.pattempts, result_get.pautorecover, notfound, str(result_get.date))
            else:
                notfound=1
                dt = datetime.now()
                dtt = dt - timedelta(days=dt.weekday())
                # The default policy (i.e. when not specified by user)
                db.insert('pw_policy', userid=id_user, date=dtt.strftime("%Y/%m/%d %H:%M:%S"),
                          plen=pwpolicy_form.default["plen"],
                          psets=pwpolicy_form.default["psets"],
                          pdict=pwpolicy_form.default["pdict"],
                          phist=pwpolicy_form.default["phist"],
                          prenew=pwpolicy_form.default["prenew"],
                          pattempts=pwpolicy_form.default["pattempts"],
                          pautorecover=pwpolicy_form.default["pautorecover"])
                result_get = db.select('pw_policy', where="userid=$id_user", vars=locals())[0]
                session.mysession.session.date = result_get.date
                return render.pwpolicy_form(session.mysession.session.user, result_get.userid, result_get.plen, result_get.psets,
                                result_get.pdict, result_get.phist, result_get.prenew,
                                result_get.pattempts, result_get.pautorecover, notfound, result_get.date)
        else:
            raise web.seeother('/login')

    def POST(self):
        web.header('Content-Type', 'application/json')
        usrid = session.mysession.session.id
        sim = simulation()
        data = json.loads(web.data())
        dat = eval(data["data"])
        if "pdict" in dat:
            dict1=1
        else:
            dat["pdict"]=0
        if "pautorecover" in dat:
            pautorecover1=1
        else:
            dat["pautorecover"]=0
        if "pattempts" in dat:
            pattempts1=1
        else:
            dat["pattempts"]=0
        pw_policy_model().update({'userid':str(usrid), 'date':data["date"]}, dat)
        for k, value in dat.iteritems():
            sim.set_policy(k, value)
#        return json.dumps(data)
        return json.dumps([{"name": "prob", "value": sim.calc_risk_prob()},
                           {"name": "impact", "value": sim.calc_risk_impact()},
                           {"name": "cost", "value": sim.calc_prod_cost()}])


class add:
    def POST(self):
        # make sure that the following line stays as per your local installation
        web.header('Content-Type', 'application/json')
        usrid = session.mysession.session.id
        sim = simulation()
#        data = json.loads(web.data())
#        dat = eval(data["data"])
#        date = data["date"]
#        dtt = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

        # get the latest date that the user has submitted a policy and add 7 days to it
        # if the user hasn't submitted anything, take today's date

        data = pwpolicy_form.default
        prev_date = datetime.strptime("2013-6-17 9", "%Y-%m-%d %H") # 9am on random Monday

        user_policies = db.select('pw_policy', where="userid=$usrid", order="date DESC", vars=locals())
        if len(user_policies) > 0:
            policy = user_policies[0] # get last policy
            prev_date = datetime.strptime(policy.date, "%Y-%m-%d %H:%M:%S")
            data = {"plen": policy.plen,
                    "psets": policy.psets,
                    "pdict": policy.pdict,
                    "phist": policy.phist,
                    "prenew": policy.prenew,
                    "pattempts": policy.pattempts,
                    "pautorecover": policy.pautorecover}
        else:
            # update to next Monday after system day as a starting date
            while prev_date < datetime.now():
                prev_date = prev_date + timedelta(days=7)

        new_date = prev_date + timedelta(days=7)

        for k, value in data.iteritems():
            sim.set_policy(k, value)

        db.insert('scores', userid=usrid, score_type=1, score_value = sim.calc_risk_prob(), date=prev_date.strftime("%Y/%m/%d %H:%M:%S"), rank=0)
        db.insert('scores', userid=usrid, score_type=2, score_value = sim.calc_prod_cost(), date=prev_date.strftime("%Y/%m/%d %H:%M:%S"), rank=0)
        return json.dumps([{"value": new_date.strftime("%Y/%m/%d %H:%M:%S")}])
