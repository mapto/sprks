__author__ = 'Horace'

import web
from localsys import storage


class authenticate:
    def check(self):
        """
        Returns user_id if client is authorized, else 0. Stub to allow other methods of authorization (eg OAuth).
        """
        auth_header = web.ctx.env.get('HTTP_AUTHORIZATION')
        user_id = storage.session.user_id

        return user_id

    def login(self, user_id):
        """
        Sets session user_id to parameter.
        """
        storage.session.user_id = user_id
        return user_id

    def logout(self):
        """
        Sets session user_id to 0.
        """
        storage.session.user_id = 0
        return 0