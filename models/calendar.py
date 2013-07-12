from models.journal import records
from sim.simulation import simulation
import web
from localsys.environment import context
from localsys.storage import db


class calendar_model:

    @classmethod
    def get_calendar(cls, user_id, data, cost, date):
        sim = simulation()

        risk = sim.calc_risk_prob()
        cost = sim.calc_prod_cost()

        calendar = records.record_prophecy(user_id, risk)

        # dtt = datetime.strptime(date, "%Y/%m/%d")
        # string_time = dtt.strftime("%Y/%m/%d")
        db.insert('scores', userid=user_id, score_type=1, score_value=risk,
                  date=date, rank=0)
        db.insert('scores', userid=user_id, score_type=2, score_value=cost,
                  date=date, rank=0)
        db.insert('pw_policy', userid=user_id, date=date,
                  plen=data["plen"], psets=data["psets"], pdict=data["pdict"], phist=data["phist"],
                  prenew=data["prenew"], pattempts=data["pattempts"], precovery=data["precovery"])
        #return json.dumps([{"value": new_date.strftime("%Y/%m/%d %H:%M:%S")}])
        return calendar
