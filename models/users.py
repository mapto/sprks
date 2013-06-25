__author__ = 'Horace'

import web
from libraries.utils import hash_utils
from environment import db
from sim.simulation import simulation


class users_model:

    def authenticate(self, username, password):
        """
        Returns ID of user if successfully authenticated, 0 otherwise.
        """
        password = hash_utils.hash_password(password)
        auth = db.select('users', where="username=$username&&password=$password", vars=locals())
        if len(auth) == 1:
            return auth[0].Id
        else:
            return 0

    def select_users(self, username):
        """
        Returns list of all users with such username.
        """
        return db.select('users', where="username=$username", vars=locals())

    def register(self, username, password, email):
        """
        Attempts to insert new user data into users table.
        Returns ID of user if successfully registered, 0 if user already exists, -1 if database error.
        """
        if len(self.select_users(username)) > 0:
            return 0
        else:
            db.insert('users', username=username, email=email, password=hash_utils.hash_password(password))
            user_lookup = self.select_users(username)
            if len(user_lookup) == 1:
                return user_lookup[0].Id
            else:
                return -1

    def update_password(self, username, password):
        """
        Updates password according to specified username and new password.
        Returns true if updated for one user, false otherwise.
        """
        if db.update('users', where="username=$username", password=hash_utils.hash_password(password), vars=locals())\
                == 1:
            return True
        else:
            return False

    def request_password(self, username, rand):
        """
        Creates password recovery ticket in pwrecovery table.
        Returns recipient email address if user found, else empty string
        """
        user_list = self.select_users(username)
        if len(user_list) == 1:
            db.insert('pwrecovery', username=username, date=web.SQLLiteral('NOW()'), rid=rand, isrecovered=0)
            # TODO detect database error?
            return user_list[0].email
        else:
            return ''

    def pwrecovery_status(self, rand):
        """
        Return username of user if password request ticket is valid. Empty string otherwise.
        """
        user_list = db.select('pwrecovery', where="rid=$rand&&isrecovered=0", vars=locals())
        # TODO inner join with 'users' table?
        if len(user_list) == 1:
            return user_list[0].username
        else:
            return ''

    def update_pwrecovery_status(self, username, success=1):
        """
        Updates password recovery ticket, assuming successful recovery.
        Returns true if one row affected, else false.
        """
        if db.update('pwrecovery', where="username=$username", isrecovered=success, vars=locals()) == 1:
            return True
        else:
            return False

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
