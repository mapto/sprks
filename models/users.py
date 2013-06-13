__author__ = 'Horace'

import hashlib
from environment import db


class users_model:

    @staticmethod
    def hash_password(password):
        """
        Hashes password for database.
        """
        return hashlib.sha224(password).hexdigest()

    def authenticate(self, username, password):
        """
        Returns ID of user if successfully authenticated, 0 otherwise.
        """
        password = self.hash_password(password)
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
            db.insert('users', username=username, email=email, password=self.hash_password(password))
            user_lookup = self.select_users(username)
            if len(user_lookup) == 1:
                return user_lookup[0].Id
            else:
                return -1