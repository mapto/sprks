from libraries import db_helper
from localsys.storage import db


class pw_policy_model:

    # Notice that the values provided here are for password policy only.
    # Values for other policies are available in models\policies.py
    ranges = {"plen": [0, 6, 8, 10, 12],
              "psets": [1, 2, 3, 4],
              "pdict": [0, 1],
              "phist": [1, 2, 3, 4],
              "prenew": [0, 1, 2, 3],
              "pattempts": [0, 1, 2],
              "precovery": [0, 1, 2]}

    bounds = {"plen": [0, 6, 12], # 0 means disabled
              "psets": [1, 4],
              "pdict": [0, 1], # categorical, thus same as range
              "phist": [1, 4],
              "prenew": [0, 3],
              "pattempts": [0, 1, 2], # categorical, thus same as range
              "precovery": [0, 1, 2]} # categorical, thus same as range

    default = {"plen": 8, "psets": 2, "pdict": 0,
               "phist": 1, "prenew": 1, "pattempts": 0,
               "precovery": 1}

    neutral = {"plen": 8, "psets": 2, "pdict": 1,
               "phist": 2, "prenew": 1, "pattempts": 1,
               "precovery": 1}

    @staticmethod
    def policy2datapoint(policy):
        """
        Gets a pw_policy dictionary
        :policy: The policy to read password policy parameters from
        Returns a tuple of password policy items. All other parameters are ignored.

        """
        return [policy["plen"], policy["psets"],
                    policy["pdict"], policy["phist"],
                    policy["prenew"], policy["pattempts"],
                    policy["precovery"]]

    @classmethod
    def update(cls, where, values):
        """
        Generates query string using db_helper.update_helper.stringify, and runs db.query.
        """
        return db.query(db_helper.update_helper.stringify('pw_policy', where, values), vars=locals())

    # This method belongs to policies, not to pw_policy
    # However, it seems that it is never used
    @classmethod
    def latest_policy(self, user_id):
        policy = {
            'location': "",
            'employee': "",
            'device': "",
            'bdata': "", # why are these strings and not numbers?
            'pdata': ""}
        policy.update(self.default)

        db_policy_all = db.select('policies', where="user_id=$user_id", order="date DESC", vars=locals())
        if len(db_policy_all) > 0:
            db_policy = db_policy_all[0]
            db_bio = db.select('biometrics', where="id=$db_policy.bio_id", vars=locals())[0]
            db_pass = db.select('passfaces', where="id=$db_policy.pass_id", vars=locals())[0]
            db_pw = db.select('pw_policy_test', where="id=$db_policy.pw_id", vars=locals())[0]
            policy["location"] = db_policy.location
            policy["employee"] = db_policy.employee
            policy["device"] = db_policy.device
            policy["bdata"] = db_bio.bdata
            policy["pdata"] = db_pass.pdata
            policy["plen"] = db_pw.plen
            policy["psets"] = db_pw.psets
            policy["pdict"] = db_pw.pdict
            policy["phist"] = db_pw.phist
            policy["prenew"] = db_pw.prenew
            policy["pattempts"] = db_pw.pattempts
            policy["precovery"] = db_pw.precovery

        return policy

    def create_variation(self, policy, id, value):
        new_policy = {}
        for key in policy:
            new_policy[key] = policy[key]
        new_policy[id] = value
        return new_policy

    def get_range(self, policy, id):
        """
        Get range of password policies for score graphs.
        """
        msgs = []
        sets = self.ranges
        for value in sets[id]:
            new_policy = self.create_variation(policy, id, value)
            msg = {}
            msg['id'] = id+str(value)
            msg["data"] = new_policy
            msgs.append(msg)
        return msgs
