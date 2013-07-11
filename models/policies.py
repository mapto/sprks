from localsys.storage import db
from localsys import environment
from copy import deepcopy
from localsys.environment import context


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

        restrict_latest = 'AND policies.date=(SELECT MAX(date) FROM policies WHERE user_id=$user_id) ' if latest else ''
        return db.query(
            'SELECT * FROM policies '
            'LEFT OUTER JOIN biometrics ON policies.bio_id = biometrics.id '
            'LEFT OUTER JOIN passfaces ON policies.pass_id = passfaces.id '
            'LEFT OUTER JOIN pw_policy ON policies.pw_id = pw_policy.id '
            'WHERE policies.user_id=$user_id ' + restrict_latest +
            'ORDER BY policies.date DESC LIMIT 27', vars=locals())

    @classmethod
    def commit_policy_update(cls, policy_update, date):
        """
        Takes a direct dump of the policyUpdate object in the request JSON, and iterates through the transaction
        logs, committing each policyDelta into the database.
        Returns None
        """
        print "parsing update policy..."
        updated_policy = policies_model().parse_policy(policy_update)
        print "done"
        print "getting latest policy from db..."
        latest_policy = policies_model().iter_to_nested_obj(policies_model().get_policy_history(4))
        print "done"
        print "merging policies..."
        merged_policy = policies_model().merge_policies(updated_policy, latest_policy)
        print "done"
        #print policies_model().nested_obj_to_list_of_dict(merged_policy)
        policies_model().insert_polices(policies_model().nested_obj_to_list_of_dict(merged_policy), date)


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

    """
    converts data from the database into nested object format
    """

    def iter_to_nested_obj(self, res):
        policy = {}
        for policies in res:
            employee = policies['employee']
            if not employee in policy.keys():
                policy[employee] = {}
            location = policies['location']
            if not location in policy[employee].keys():
                policy[employee][location] = {}
            device = policies['device']
            if not device in policy[employee][location].keys():
                policy[employee][location][device] = {}
            policy[employee][location][device]['id'] = policies['id_policy']
            policy[employee][location][device]['pwpolicy'] = {}
            policy[employee][location][device]['passfacepolicy'] = {}
            policy[employee][location][device]['biopolicy'] = {}
            for key in policies:
                if key == 'bio_id' or key == 'pw_id' or key == 'date' or key == 'id_policy' or key == 'pass_id':
                    continue
                if key == 'pdata':
                    policy[employee][location][device]['passfacepolicy'][key] = str(policies[key])
                if key == 'bdata':
                    policy[employee][location][device]['biopolicy'][key] = policies[key]
                if key == 'prenew' or key == 'pdict' or key == 'psets' or key == 'precovery' or key == 'plen'\
                    or key == 'phist' or key == 'pattempts':
                    policy[employee][location][device]['pwpolicy'][key] = policies[key]
        return policy

    """
    Merges two policies
    """

    def merge_policies(self, updated_policy, old_policy):
        tmp_policy = deepcopy(old_policy)
        for employee in updated_policy:
                for location in updated_policy[employee]:
                    for device in updated_policy[employee][location]:
                        for policy in updated_policy[employee][location][device]:
                                if updated_policy[employee][location][device][policy] == {}:
                                    for key, value in tmp_policy[employee][location][device][policy].iteritems():
                                        tmp_policy[employee][location][device][policy][key] = 0
                                else:
                                    for key, value in updated_policy[employee][location][device][policy].iteritems():
                                        tmp_policy[employee][location][device][policy][key] = value
        return tmp_policy

    """
    converts nested object into list of dictionaries
    """

    def nested_obj_to_list_of_dict(self, policies):
        #tmp_obj = {}
        policies_list = []
       # data = {}
        for employee in policies:
            data = {}
            tmp_obj = {}
            data['employee'] = employee
            for location in policies[employee]:
                data['location'] = location
                for device in policies[employee][location]:
                    data['device'] = device
                    for policy in policies[employee][location][device]:
                        if policy == 'id':
                            tmp_obj['id'] = policies[employee][location][device][policy]
                        else:
                            for key, value in policies[employee][location][device][policy].iteritems():
                                data[key] = value
                            tmp_obj['data'] = deepcopy(data)
                    policies_list.append(deepcopy(tmp_obj))
        return policies_list

    """
    Checks if password mechanism is used or not
    """

    def check_default(self, policy):
        pdict = policy['pdict']
        if pdict == 'true':
            return 1
        elif pdict == 'false':
            pdict = 0
        return policy['plen']+policy['psets']+policy['phist']+policy['pattempts']+pdict+policy['prenew']

    """
    Inserts separate row(policy) into table
    """

    def insert_into_tables(self, policy, date):
        if self.check_default(policy) == 0:
            id_pwpolicy = 0
        else:
            id_pwpolicy = db.insert('pw_policy', plen=policy['plen'], psets=policy['psets'], pdict=policy['pdict'],
                                    phist=policy['phist'], prenew=policy['prenew'], pattempts=policy['pattempts'],
                                    precovery=policy['precovery'])
        db.insert('policies', user_id=4, location=policy['location'],
                              employee=policy['employee'], device=policy['device'], bio_id=policy['bdata'],
                              pass_id=policy['pdata'], pw_id=id_pwpolicy, date=date)

    """
    Inserts set of policies into table
    """

    def insert_polices(self, policies, date):
        for policy in policies:
            self.insert_into_tables(policy['data'], date)
            #print policy

