__author__ = 'Daniyar'

from models.journal import records
from sim.simulation import simulation
import web
from localsys.environment import context
from localsys.storage import db


class calendar_model:

    @classmethod
    def get_calendar(cls, data, cost, date):
        web.header('Content-Type', 'application/json')
        usrid = context.user_id()
        sim = simulation()
        post_data = data
        policy = post_data

        for k, value in policy.iteritems():
            sim.set_policy(k, value)

        validation = records().validate_ournal(cost, date, usrid)  #0-if validation failed, 1-otherwise

        risk = sim.calc_risk_prob()
        cost = sim.calc_prod_cost()

        calendar = records().update_journal(risk, usrid)  #inserts new events into journal

        # dtt = datetime.strptime(date, "%Y/%m/%d")
        # string_time = dtt.strftime("%Y/%m/%d")
        db.insert('scores', userid=usrid, score_type=1, score_value=risk,
                  date=date, rank=0)
        db.insert('scores', userid=usrid, score_type=2, score_value=cost,
                  date=date, rank=0)
        db.insert('pw_policy', userid=usrid, date=date,
                  plen=data["plen"], psets=data["psets"], pdict=data["pdict"], phist=data["phist"],
                  prenew=data["prenew"], pattempts=data["pattempts"], precovery=data["precovery"])
        #return json.dumps([{"value": new_date.strftime("%Y/%m/%d %H:%M:%S")}])
        return calendar
