__author__ = 'Horace'

import web
from libraries.utils import hash_utils
from environment import db


class users_model:

    def get_username(self, user_id):
        """
        Returns username of user given user_id, empty string otherwise.
        """
        users = db.select('users', where="user_id=$user_id", vars=locals())
        if len(users) == 1:
            return users[0].username
        else:
            return ''


    def authenticate(self, username, password):
        """
        Returns ID of user if successfully authenticated, 0 otherwise.
        """
        password = hash_utils.hash_password(password)
        auth = db.select('users', where="username=$username&&password=$password", vars=locals())
        if len(auth) == 1:
            return auth[0].user_id
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
                return user_lookup[0].user_id
            else:
                return -1

    def update_password(self, username, password):
        """
        Updates password according to specified username and new password.
        Returns true if updated for one user, false otherwise.
        """
        # TODO should take user_id instead
        if db.update('users', where="username=$username", password=hash_utils.hash_password(password), vars=locals())\
                == 1:
            return True
        else:
            return False

    def request_password(self, username, rand):
        """
        Creates password recovery ticket in password_recovery table.
        Returns recipient email address if user found, else empty string
        """
        # TODO should take user_id instead
        user_list = self.select_users(username)
        if len(user_list) == 1:
            db.insert('password_recovery', username=username, date=web.SQLLiteral('NOW()'), rid=rand, isrecovered=0)
            # TODO detect database error?
            return user_list[0].email
        else:
            return ''

    def password_recovery_status(self, rand):
        """
        Return username of user if password request ticket is valid. Empty string otherwise.
        """
        user_list = db.select('password_recovery', where="rid=$rand&&isrecovered=0", vars=locals())
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
