__author__ = 'mruskov'

import web
import json
import session
from sim.simulation import simulation
from datetime import timedelta, datetime
from environment import db
from pwpolicy import pwpolicy

class forward:
    def POST(self):
        # make sure that the following line stays as per your local installation
        web.header('Content-Type', 'application/json')
        usrid = session.mysession.session.id
        sim = simulation()

        # get the latest date that the user has submitted a policy and add 7 days to it
        # if the user hasn't submitted anything, take today's date
        data = pwpolicy.default
        prev_date = datetime.strptime("2014-1-6 9", "%Y-%m-%d %H") # 9am on 6 January 2014

        user_policies = db.select('pw_policy', where="userid=$usrid", order="date DESC", vars=locals())
        if len(user_policies) > 0:
            policy = user_policies[0] # get last policy
            prev_date = policy.date
            data = {"plen": policy.plen,
                    "psets": policy.psets,
                    "pdict": policy.pdict,
                    "phist": policy.phist,
                    "prenew": policy.prenew,
                    "pattempts": policy.pattempts,
                    "pautorecover": policy.pautorecover}
        # If we have a dynamic starting date. Fancy, but client does a check for the starting date
        # else:
        #     # update to next Monday after system day as a starting date
        #     while prev_date < datetime.now():
        #         prev_date = prev_date + timedelta(days=7)

        new_date = prev_date + timedelta(days=7)

        for k, value in data.iteritems():
            sim.set_policy(k, value)

        db.insert('scores', userid=usrid, score_type=1, score_value = sim.calc_risk_prob(), date=prev_date.strftime("%Y/%m/%d %H:%M:%S"), rank=0)
        db.insert('scores', userid=usrid, score_type=2, score_value = sim.calc_prod_cost(), date=prev_date.strftime("%Y/%m/%d %H:%M:%S"), rank=0)
        db.insert('pw_policy', userid=usrid, date=new_date.strftime("%Y/%m/%d %H:%M:%S"),
                  plen=data["plen"], psets=data["psets"], pdict=data["pdict"], phist=data["phist"],
                  prenew=data["prenew"], pattempts=data["pattempts"], pautorecover=data["pautorecover"])
        return json.dumps([{"value": new_date.strftime("%Y/%m/%d %H:%M:%S")}])
