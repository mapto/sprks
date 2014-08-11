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
            value = auth[0]
            id = value.Id
            return id
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
            db.insert('users', username=username, email=email, password=hash_utils.hash_password(password), game_turn=0)
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

    def get_turn(self, username):
        result = db.select('users', where="username=$username", vars=locals())
        if len(result) == 1:
            entry = result[0]
            turn = entry.game_turn
            return turn
        else:
            raise Exception("Unable to read user's turn")
            # return 0

    def end_turn(self, username):
        new_turn = self.get_turn(username) + 1;
        db.update(tables='users', where="username=$username", vars=locals(), game_turn=new_turn);
        print "end turn" + str(new_turn)
        return new_turn

    def end_game(self, username):
        new_turn = 0;
        db.update(tables='users', where="username=$username", vars=locals(), game_turn=new_turn);
        print "end game" + str(new_turn)
        return new_turn
