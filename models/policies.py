from localsys.storage import db
from localsys import environment
from copy import deepcopy
from localsys.environment import context
from pprint import pprint



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
        :param user_id: user_id of user to get policies for
        :param latest: flag limits to only getting the latest set of policies
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
    def policies_equal(cls, policy1, policy2):
        skipped = ["user_id", "bio_id", "pw_id", "pass_id", "date", "employee", "device", "location", "id_policy"]
        for key in policy1:
            if key in skipped:
                continue
            if policy1[key] != policy2[key]:
                return False

        return True

    @classmethod
    def get_compressed_policy(cls, user_id):
        policies = policies_model.get_policy_history(user_id, latest=True)
        skipped = ["user_id", "bio_id", "pw_id", "pass_id", "date", "employee", "device", "location", "id_policy"]
        environmental = ["employee", "location", "device"]

        env = {}
        added = False
        for new_policy in policies:
            for key in env:
                stored_policy = env[key]
                #TODO handle logic for multiple env vars(i.e. locations/devices/employees)
                if policies_model.policies_equal(new_policy, stored_policy):
                    for next in environmental:
                        if new_policy[next] not in stored_policy[next]:
                            stored_policy[next].add(new_policy[next])
                    added = True
                    break

            if not added:
                i = int(new_policy['id_policy'])
                env[i] = {}
                for key in new_policy:
                    if key in skipped:
                        continue
                    env[i][key] = new_policy[key]
                print env[i]
                env[i]['employee'] = [new_policy['employee']]
                env[i]['location'] = [new_policy['location']]
                env[i]['device'] = [new_policy['device']]


        return env

    @classmethod
    def commit_policy_update(cls, policy_update, date):
        """
        Takes a direct dump of the policyUpdate object in the request JSON, and iterates through the transaction
        logs, committing each policyDelta into the database.
        Returns None
        :param policy_update:
        :param date:
        """
        print "parsing update policy..."
        updated_policy = policies_model().parse_policy(policy_update)
        print "done"
        print "getting latest policy from db..."
        latest_policy = policies_model().iter_to_nested_obj(policies_model().get_policy_history(context.user_id()))
        print "done"
        print "merging policies..."
        merged_policy = policies_model().merge_policies(updated_policy, latest_policy)
        print "done"
        #print policies_model().nested_obj_to_list_of_dict(merged_policy)
        policies_model().insert_polices(policies_model().nested_obj_to_list_of_dict(merged_policy), date)


    def parse_policy(self, policyUpdate):
        """
        converts data from the database into nested object format
        """
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

    def iter_to_nested_obj(self, res):
        """
        Merges two policies
        :param res:
        """
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
            policy[employee][location][device]['passfaces'] = {}
            policy[employee][location][device]['biometric'] = {}
            for key in policies:
                if key == 'bio_id' or key == 'pw_id' or key == 'date' or key == 'id_policy' or key == 'pass_id':
                    continue
                if key == 'pdata':
                    policy[employee][location][device]['passfaces'][key] = str(policies[key])
                if key == 'bdata':
                    policy[employee][location][device]['biometric'][key] = policies[key]
                if key == 'prenew' or key == 'pdict' or key == 'psets' or key == 'precovery' or key == 'plen'\
                    or key == 'phist' or key == 'pattempts':
                    policy[employee][location][device]['pwpolicy'][key] = policies[key]
        return policy

    def merge_policies(self, updated_policy, old_policy):
        """
        converts nested object into list of dictionaries
        :param updated_policy:
        :param old_policy:
        """
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

    def nested_obj_to_list_of_dict(self, policies):
        """
        Checks if password mechanism is used or not
        :param policies:
        """
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

    def check_default(self, policy):
        """
        Inserts separate row(policy) into table
        """

        """ pdict = policy['pdict']
        if pdict == 'true':
            return 1
        elif pdict == 'false':
            pdict = 0"""
        print policy
        return int(policy['plen'])+int(policy['psets'])+int(policy['phist'])+int(policy['pattempts'])+int(policy['pdict'])+int(policy['prenew'])



    def insert_into_tables(self, policy, date):
        """
        Inserts set of policies into table
        """
        if self.check_default(policy) == 0:
            id_pwpolicy = 0
        else:
            id_pwpolicy = db.insert('pw_policy', plen=policy['plen'], psets=policy['psets'], pdict=policy['pdict'],
                                    phist=policy['phist'], prenew=policy['prenew'], pattempts=policy['pattempts'],
                                    precovery=policy['precovery'])
        db.insert('policies', user_id=context.user_id(), location=policy['location'],
                              employee=policy['employee'], device=policy['device'], bio_id=policy['bdata'],
                              pass_id=policy['pdata'], pw_id=id_pwpolicy, date=date)



    def insert_polices(self, policies, date):
        for policy in policies:
            self.insert_into_tables(policy['data'], date)
            #print policy

    def get_policies_list(self, user_id):
        latest_policies = self.get_policy_history(user_id)
        print len(latest_policies)
        policies = []
        #date = latest_policies[0].date
        for row in latest_policies:
            policy = {}
            for key, value in row.iteritems():
                if key == 'id_policy' or key == 'bio_id' or key == 'pw_id' or key == 'id' or key == 'user_id' or \
                                key == 'pass_id':
                    continue
                if key == 'date':
                    date = value
                else:
                    policy[key] = value
            policies.append(deepcopy(policy))
        response = {'policyAccept': True,
                    'interventionAccept': True,
                    'calendar': [{}],
                    'policy': policies,
                    'date': date
                    }
        return response



if __name__ == "__main__":
    print policies_model.get_compressed_policy(1)
