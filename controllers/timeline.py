__author__ = 'mruskov'

import web
import json
import session
from sim.simulation import simulation
from environment import db
from pwpolicy import pwpolicy
from environment import render_public as render
from models import users


class timeline:

    def GET(self):
        return render.timeline()


class forward:
    def POST(self):
        # make sure that the following line stays as per your local installation
        web.header('Content-Type', 'application/json')
        usrid = session.mysession.session.id
        sim = simulation()

        # get the latest date that the user has submitted a policy and add 7 days to it
        # if the user hasn't submitted anything, take today's date
        data = pwpolicy.default
        prev_date = session.mysession.session.turn  # needed only if user can press /forward without having seen the policy page

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
                    "precovery": policy.precovery}
        # If we have a dynamic starting date. Fancy, but client does a check for the starting date
        # else:
        #     # update to next Monday after system day as a starting date
        #     while prev_date < datetime.now():
        #         prev_date = prev_date + timedelta(days=7)

        new_date = users.users_model().end_turn(session.mysession.session.user)
        if new_date > 13:
            session.mysession.session.turn = users.users_model().end_game(session.mysession.session.user)
        else:
            session.mysession.session.turn = new_date

        for k, value in data.iteritems():
            sim.set_policy(k, value)

        db.insert('scores', userid=usrid, score_type=1, score_value = sim.get_risk(data), date=prev_date, rank=0)
        db.insert('scores', userid=usrid, score_type=2, score_value = sim.calc_prod_cost(data), date=prev_date, rank=0)
        db.insert('pw_policy', userid=usrid, date=new_date,
                  plen=data["plen"], psets=data["psets"], pdict=data["pdict"], phist=data["phist"],
                  prenew=data["prenew"], pattempts=data["pattempts"], precovery=data["precovery"])
        return json.dumps([{"value": new_date}])
