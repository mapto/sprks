__author__ = 'Horace'

import web
import environment


class auth:
    def user_id(self):
        """
        Returns user_id if client is authorized, else 0. Potentially allows other methods of authorization (eg OAuth).
        """
        auth_header = web.ctx.env.get('HTTP_AUTHORIZATION')
        if environment.session.user_id > 0:
            return environment.session.user_id
        return self.http_auth(auth_header);

    def http_auth(self, auth_header):
        return 0
