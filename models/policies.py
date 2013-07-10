from localsys.storage import db
from sim.simulation import simulation
from localsys import environment


class policies_model:

    @classmethod
    def populate_policies(cls, user_id, date):
        employee_types = {'executives', 'desk', 'road'}
        location_types = {'office', 'public', 'home'}
        device_types = {'desktop', 'laptop', 'phone'}

        values = []
        for employee in employee_types:
            for location in location_types:
                for device in device_types:
                    values.append(
                        {
                            'user_id': user_id,
                            'location': location,
                            'employee': employee,
                            'device': device,
                            'date': environment.start_date
                        }
                    )
        db.multiple_insert('policies', values)
        #TODO

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

    @classmethod
    def get_latest_policy(cls, user_id):
        """
        Doc stub
        """
        return db.select('SELECT * FROM pw_policy'
                        'OUTER JOIN biometrics ON policy.bioid=biometrics.id'
                        'OUTER JOIN passface ON policy.passid=passface.id'
                        'OUTER JOIN pw_policy ON policy.pwid=pw_policy.id'
                        'WHERE policies.user_id=$user_id AND policies.date=MAX(policies.date) LIMIT 27', vars=locals())