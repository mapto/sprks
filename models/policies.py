from localsys.storage import db
from localsys import environment
from copy import deepcopy
from localsys.environment import context
import models.company
from models.pw_policy import pw_policy_model


class policies_model:
    """
    This class takes care of all policies that do not have dedicated models (currently all except pw_policies)
    It should provide the same features to be used from modules that require a policy
    """
    non_pw_ranges = {"bdata": [0, 1, 2], "pdata": [0, 1, 2]}
    non_pw_bounds = non_pw_ranges # for categorical data each value defines the bounds
    non_pw_default = {"bdata": 0, "pdata": 0} # default values are used to set initial policy
    non_pw_neutral = non_pw_default # neutral values are the ones that are expected to minimally affect cost and risk

    @classmethod
    def get_bounds(cls):
        result = pw_policy_model.bounds.copy()
        result.update(policies_model.non_pw_bounds)
        return result

    @classmethod
    def get_ranges(cls):
        result = pw_policy_model.ranges.copy()
        result.update(policies_model.non_pw_ranges)
        return result

    @classmethod
    def get_default(cls):
        result = pw_policy_model.default.copy()
        result.update(policies_model.non_pw_default)
        return result

    @classmethod
    def get_neutral(cls):
        result = pw_policy_model.neutral.copy()
        result.update(policies_model.non_pw_neutral)
        return result

    @staticmethod
    def policy2datapoint(policy):
        """
        Handles policies, distinguishing parameters that should be considered as part of the policy and ones that are independent
        :policy: The policy to read password policy parameters from
        Returns a tuple of password policy items. All other parameters are ignored.
        """
        tmp_policy = deepcopy(policy)
        if not 'bdata' in policy:
            tmp_policy['bdata'] = 0
        if not 'pdata' in policy:
            tmp_policy['pdata'] = 0
        result = [tmp_policy["bdata"], tmp_policy["pdata"]]
        result.extend(pw_policy_model.policy2datapoint(policy))
        return result

    @classmethod
    def populate_policies(cls, user_id, date):
        """
        Populates policies (27 rows) for new users. Returns the list of ids of the inserted rows.
        """
        employee_types = models.company.company.employee_types
        location_types = models.company.company.location_types
        device_types = models.company.company.device_types

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
        results_list = []
        restrict_latest = 'AND policies.date=(SELECT MAX(date) FROM policies WHERE user_id=$user_id) ' if latest else ''
        res = db.query(
            'SELECT * FROM policies '
            'LEFT OUTER JOIN biometrics ON policies.bio_id = biometrics.id '
            'LEFT OUTER JOIN passfaces ON policies.pass_id = passfaces.id '
            'LEFT OUTER JOIN pw_policy ON policies.pw_id = pw_policy.id '
            'WHERE policies.user_id=$user_id ' + restrict_latest +
            'ORDER BY policies.date DESC LIMIT 324', vars=locals())
            # Why are policies limited to 54? Shouldn't they be 27 (3x3x3)?

        for row in res:
            tmp = {}
            for key, value in row.iteritems():
                tmp[key] = str(value)
            results_list.append(tmp)
        return results_list

    @classmethod
    def policies_equal(cls, policy1, policy2):
        skipped = ["user_id", "bio_id", "pw_id", "pass_id", "date", "employee", "device", "location", "id_policy"]
        for key in policy1:
            if key not in skipped and policy1[key] != policy2[key]:
                return False

        return True

    @classmethod
    def get_compressed_policy(cls, user_id):
        # TODO currently not used. The issue below needs to be fixed before this can be used
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
                    for dimension in environmental:
                        if new_policy[dimension] not in stored_policy[dimension]:
                            stored_policy[dimension].add(new_policy[dimension])
                    added = True
                    break

            if not added:
                i = int(new_policy['id_policy'])
                env[i] = {}
                for key in new_policy:
                    if key in skipped:
                        continue
                    env[i][key] = new_policy[key]
                print(env[i])
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
        print("parsing update policy...")
        updated_policy = policies_model().parse_policy(policy_update)
        print("done")
        print("getting latest policy from db...")
        latest_policy = policies_model().iter_to_nested_obj(policies_model().get_policy_history(context.user_id(), True))
        print(latest_policy)
        print("done")
        print("merging policies...")
        merged_policy = policies_model().merge_policies(updated_policy, latest_policy)
        print("done")
        print("inserting into table")
        #print policies_model().nested_obj_to_list_of_dict(merged_policy)
        policies_model().insert_polices(policies_model().nested_obj_to_list_of_dict(merged_policy), date)
        print("done")

    @classmethod
    def commit_same_policy(cls, date):
        """
        Gets the latest policy set from the server and duplicates them for the specified date.
        """
        print("getting latest policy from db...")
        latest_policy = policies_model().iter_to_nested_obj(policies_model().get_policy_history(context.user_id()))
        print("done")
        print("inserting into table")
        policies_model().insert_polices(policies_model().nested_obj_to_list_of_dict(latest_policy), date)
        print("done")

    def parse_policy(self, policyUpdate):
        """
        Converts client-submitted policyUpdate changes to proprietary nested object format.
        :param policyUpdate: policy updates from client
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
        Converts iterator returned from SQL query into nested object
        :param res: iterator
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
                if key == 'prenew' or key == 'pdict' or key == 'psets' or key == 'precovery' or \
                        key == 'plen' or key == 'phist' or key == 'pattempts':
                    policy[employee][location][device]['pwpolicy'][key] = policies[key]
        return policy

    def merge_policies(self, updated_policy, old_policy):
        """
        Merges old policy from database with updated policy from client into one nested object
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
                                if key == 'plen' and value == '0':
                                    tmp_policy[employee][location][device]['pwpolicy']['psets'] = 1
                                    tmp_policy[employee][location][device]['pwpolicy']['pdict'] = 0
                                    tmp_policy[employee][location][device]['pwpolicy']['phist'] = 0
                                    tmp_policy[employee][location][device]['pwpolicy']['prenew'] = 0
                                    tmp_policy[employee][location][device]['pwpolicy']['pattempts'] = 0
                                    tmp_policy[employee][location][device]['pwpolicy']['precovery'] = 0
                                    break
        return tmp_policy

    def nested_obj_to_list_of_dict(self, policies):
        """
        Converts nested object (e.g {'executive: {'home': {'phone': {...}}}'} ) into a list of dictionary:
        [{'employee':'executives', 'location': 'home', 'device': 'phone',...}]
        :param policies: nested object that represent policy
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
        Checks if password mechanism is used or not
        :param policies: password policy
        """

        # pdict = policy['pdict']
        # if pdict == 'true':
        #     return 1
        # elif pdict == 'false':
        #     pdict = 0

        return int(policy['plen']) + int(policy['psets']) + int(policy['phist']) + int(policy['pattempts'])\
            + int(policy['pdict']) + int(policy['prenew'])

    def insert_into_tables(self, policy, date):
        """
        Inserts set of policies into table
        """
        print("policy inside insert_into_tables")
        print(policy)
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

    @classmethod
    def get_policies_list(cls, user_id):
        """
        Given user_id, returns the latest policies set.
        """
        latest_policies = cls.get_policy_history(user_id, latest=True)
        policies = []
        #date = latest_policies[0].date
        for row in latest_policies:
            policy = {}
            id_keys = ['id_policy', 'bio_id', 'pw_id', 'id', 'user_id', 'pass_id']
            for key, value in row.iteritems():
                if key in id_keys:
                    continue
                if key == 'date':
                    date = value
                else:
                    policy[key] = value
            policies.append(deepcopy(policy))

        return policies
