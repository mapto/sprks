from localsys.storage import db
from sim.simulation import simulation
from localsys import environment


class policies_model:

    @classmethod
    def populate_policies(cls, user_id, date):
        """
        Populates policies (27 rows) for new users. Returns the list of ids of the inserted rows.
        """
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
        return db.multiple_insert('policies', values)

    @classmethod
    def get_policy_history(cls, user_id, latest=False):
        """
        Returns list of past policies set by user.
        """

        restrict_latest = 'AND policies.date=(SELECT MAX(date) FROM policies WHERE user_id=11) ' if latest else ''
        return db.select(
            'SELECT * FROM policies '
            'LEFT OUTER JOIN biometrics ON policies.bio_id = biometrics.id '
            'LEFT OUTER JOIN passfaces ON policies.pass_id = passfaces.id '
            'LEFT OUTER JOIN pw_policy ON policies.pw_id = pw_policy.idpolicy '
            'WHERE policies.user_id=$user_id ' + restrict_latest +
            'ORDER BY policies.date DESC LIMIT 27', vars=locals())

        #
        # results = db.select('pw_policy', where="userid=$user_id", order="date", vars=locals())
        # history = []
        # sim = simulation()
        # for row in results:
        #     tmp = {}
        #     for k, v in row.iteritems():
        #         tmp[k] = str(v)
        #         if k != 'idpolicy' and k != 'userid' and k != 'date':
        #             sim.set_policy(k, v)
        #     tmp['risk'] = sim.calc_risk_prob()
        #     tmp['cost'] = sim.calc_prod_cost()
        #     history.append(tmp)
        # return history

    @classmethod
    def get_latest_policy(cls, user_id):
        """
        Gets latest policy
        """
        return cls.get_policy_history(user_id, latest=True)