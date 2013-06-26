__author__ = 'Horace'

from environment import db
from sim.simulation import simulation


class policies_model:

    def get_policy_history(self, id):
        history = db.select('pw_policy', where="userid=$id", order="date", vars=locals())
        history_dict = []
        sim = simulation()
        for row in history:
            tmp = {}
            for k, v in row.iteritems():
                tmp[k] = str(v)
                if k != 'idpolicy' and k != 'userid' and k != 'date':
                    sim.set_policy(k, v)
            tmp['risk'] = sim.calc_risk_prob()
            tmp['cost'] = sim.calc_prod_cost()
            history_dict.append(tmp)
        return history_dict
