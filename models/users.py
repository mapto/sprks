__author__ = 'Horace'

import hashlib


class users_model:

    def authenticate(self, username, password):
        password = hashlib.sha224(password).hexdigest()
        return self.db.select('users', where="username=$username&&password=$password", vars=locals())