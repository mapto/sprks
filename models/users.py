__author__ = 'Horace'

import web
from libraries.utils import hash_utils
from environment import db


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

    def request_password(self, username, rand):
        """
        Creates password recovery entry in pwrecovery table.
        Returns recipient email address if user found, else empty string
        """
        user_list = users_model.select_users(username)
        if len(user_list) == 1:
            db.insert('pwrecovery', username=username, date=web.SQLLiteral('NOW()'), rid=rand, isrecovered=0)
            # TODO detect database error?
            return user_list[0].email
        else:
            return ''