from localsys.storage import db
from sim.simulation import simulation


class policies_model:
    @classmethod
    def get_policy_history(cls, user_id):
        """
        Returns list of past policies set by user.
        """
        # TODO potential performance/memory bug
        results = db.select('pw_policy', where="userid=$user_id", order="date", vars=locals())
        history = []
        sim = simulation()
        for row in results:
            tmp = {}
            for k, v in row.iteritems():
                tmp[k] = str(v)
                if k != 'idpolicy' and k != 'userid' and k != 'date':
                    # TODO bad bad bad
                    sim.set_policy(k, v)
            tmp['risk'] = sim.calc_risk_prob()
            tmp['cost'] = sim.calc_prod_cost()
            history.append(tmp)
        return history

    def get_latest_policy(self, user_id):
        """
        Doc stub
        """
        results = db.select('pw_policy', where="userid=$user_id", order="date", vars=locals())[0]
        policy = {}
        for k, value in results.iteritems():
            if k != 'idpolicy' and k != 'userid' and k != 'date':
                policy[k] = str(value)
        return policy