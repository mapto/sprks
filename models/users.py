import web
from libraries.utils import hash_utils
from localsys.storage import db
import localsys
from localsys import storage

import re
import base64


class users_model:

    @classmethod
    def authorize(cls):
        """
        Returns user_id if request is authorized, else 0.
        Authorizes by checking the following in order:
        1. HTTP Authorization header
        2. Session data
        """

        if web.ctx.env.get('HTTP_AUTHORIZATION') is None:
            # Do not use context cache - will cause infinite recursion.
            return storage.session.user_id
        else:
            auth = re.sub('^Basic ','',web.ctx.env.get('HTTP_AUTHORIZATION'))
            username, password = base64.decodestring(auth).split(':')
            return users_model.check_credentials(username, password)

    @classmethod
    def session_login(cls, user_id):
        """
        Sets session user_id to parameter.
        """
        localsys.storage.session.user_id = user_id

        # Can't guarantee this method will be used before cache is initialized.
        localsys.environment.context.flush_cache()

        return user_id

    @classmethod
    def get_username(cls, user_id):
        """
        Returns username of user given user_id, empty string otherwise.
        """
        users = db.select('users', where="user_id=$user_id", vars=locals())
        if len(users) == 1:
            return users[0].username
        else:
            return ''

    @classmethod
    def get_user_id(cls, username):
        """
        Returns user_id given username, 0 otherwise.
        """
        users = db.select('users', where="username=$username", vars=locals())
        if len(users) == 1:
            return users[0].user_id
        else:
            return 0

    @classmethod
    def check_credentials(cls, username, password):
        """
        Returns ID of user if credentials match, 0 otherwise.
        """
        password = hash_utils.hash_password(password)
        auth = db.select('users', where="username=$username&&password=$password", vars=locals())
        if len(auth) == 1:
            return auth[0].user_id
        else:
            return 0

    @classmethod
    def select_users(cls, user_id=0, username=''):
        """
        Returns list of all users with 'username' and 'user_id' (optional) parameters.
        """
        if user_id > 0:
            if username != '':
                return db.select('users', where="username=$username&&user_id=$user_id", vars=locals())
            else:
                return db.select('users', where="user_id=$user_id", vars=locals())
        else:
            return db.select('users', where="username=$username", vars=locals())

    @classmethod
    def register(cls, username, password, email):
        """
        Attempts to insert new user data into users table.
        Returns ID of user if successfully registered, 0 if user already exists, -1 if database error.
        """
        if len(cls.select_users(username=username)) > 0:
            return 0
        else:
            if username == '' or email == '':
                return -1
            db.insert('users', username=username, email=email, password=hash_utils.hash_password(password))
            user_lookup = cls.select_users(username=username)
            if len(user_lookup) == 1:
                return user_lookup[0].user_id
            else:
                return -1

    @classmethod
    def update_password(cls, user_id, password):
        """
        Updates password according to specified user_id and new password.
        Returns true if updated for one user or password unchanged, false otherwise.
        """
        user_list = cls.select_users(user_id=user_id)
        password_hash = hash_utils.hash_password(password)
        if len(user_list) == 1 and password_hash == user_list[0].password:
            return True

        if db.update('users', where="user_id=$user_id", password=password_hash, vars=locals()) \
                == 1:
            return True

        return False

    @classmethod
    def request_password(cls, token, user_id):
        """
        Creates password recovery ticket in password_recovery table.
        Returns recipient email address if user found, else empty string
        """
        user_list = cls.select_users(user_id=user_id)
        if len(user_list) == 1:
            user = user_list[0]
            db.insert('password_recovery', user_id=user.user_id, date=web.SQLLiteral('NOW()'), token=token, invalid=0)
            return user.email
        else:
            return ''

    @classmethod
    def password_recovery_user(cls, token):
        """
        Return user_id if password request ticket is valid. 0 otherwise.
        :param token:
        """
        user_list = db.select('password_recovery', where="token=$token&&invalid=0", vars=locals())
        if len(user_list) == 1:
            return user_list[0].user_id
        else:
            return 0

    @classmethod
    def update_recovery_status(cls, token, invalid=1):
        """
        Updates password recovery ticket, assuming successful recovery.
        Returns true if one row affected, else false.
        """
        if db.update('pwrecovery', where="token=$token", invalid=invalid, vars=locals()) == 1:
            return True
        else:
            return False
