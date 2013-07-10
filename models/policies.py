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
                            'date': environment.start_date,
                            'bio_id': 0,
                            'pass_id': 0,
                            'pw_id': 0
                        }
                    )
        return db.multiple_insert('policies', values)

    @classmethod
    def get_policy_history(cls, user_id, latest=False):
        """
        Returns list of past policies set by user.
        """

        restrict_latest = 'AND policies.date=(SELECT MAX(date) FROM policies WHERE user_id=11) ' if latest else ''
        return db.query(
            'SELECT * FROM policies '
            'LEFT OUTER JOIN biometrics ON policies.bio_id = biometrics.id '
            'LEFT OUTER JOIN passfaces ON policies.pass_id = passfaces.id '
            'LEFT OUTER JOIN pw_policy ON policies.pw_id = pw_policy.id '
            'WHERE policies.user_id=$user_id ' + restrict_latest +
            'ORDER BY policies.date DESC LIMIT 27', vars=locals())

    @classmethod
    def get_latest_policy(cls, user_id):
        """
        Gets latest policy
        """
        #return db.query('SELECT * FROM policies LEFT OUTER JOIN biometrics ON policies.bio_id = biometrics.id LEFT OUTER JOIN passfaces ON policies.pass_id = passfaces.id LEFT OUTER JOIN pw_policy ON policies.pw_id = pw_policy.idpolicy WHERE policies.user_id =1 LIMIT 27', vars=locals())
        return cls.get_policy_history(user_id, latest=False)

    def parse_policy(self, policyUpdate):
        policies = {}
        for update in policyUpdate:
            for empl in update['employee']:
                if not empl in policies.keys():
                    policies[empl] = {}
                for loc in update['location']:
                    if not loc in policies[empl].keys():
                        policies[empl][loc] = {}
                    for dev in update['device']:
                        if not dev in policies[empl][loc].keys():
                            policies[empl][loc][dev] = {}
                        for key, value in update['policyDelta'].iteritems():
                            policies[empl][loc][dev][key] = {}
                            if not value == {}:
                                for k, v in value.iteritems():
                                    policies[empl][loc][dev][key][k] = v
                            #policies[empl][loc][dev][key] = value
        return policies

    @classmethod
    def iter_to_dict(self, policies):
        policy = {}
        for key in policies:
            if key == 'bio_id' or key == 'pw_id' or key == 'date' or key == 'id' or key == 'pass_id':
                continue
            employee = policies['employee']
            policy[employee] = {}
            location = policies['location']
            policy[employee][location] = {}
            device = policies['device']
            policy[employee][location][device] = {}
            policy[employee][location][device]['pwpolicy'] = {}
            policy[employee][location][device]['passfacepolicy'] = {}
            policy[employee][location][device]['biopolicy'] = {}
            if key is 'pdata':
                policy[employee][location][device]['passfacepolicy'][key] = str(policies[key])
            if key is 'bdata':
                policy[employee][location][device]['biopolicy'][key] = policies[key]
            if key == 'prenew' or key == 'pdict' or key == 'psets' or key == 'precovery' or key == 'plen'\
                or key == 'phist' or key == 'pattempts':
                policy[employee][location][device]['pwpolicy'][key] = policies[key]
        return policy

if __name__ == "__main__":
    row = policies_model.get_latest_policy(4)[0]
#for row in res:
#for k, v in row.iteritems():
#    print k, v
    #print row
    for field in row:
        print field + ":" + str(row[field])
    print policies_model.iter_to_dict(row)
    print row['pdata']
        #for k in field:
        #    print k