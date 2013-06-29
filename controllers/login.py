
__author__ = "Dan"

import web
import environment
from environment import render_public as render
from models.users import users_model


class login:
    """ Controllers commonly need a reference to the model (db) and also views
       These are declared in environment
    """

    def GET(self):
        environment.session.user_id = 0
        return render.login()

    def POST(self):
        request = web.input()
        user_id = users_model().authenticate(request.username, request.password)
        if user_id > 0:
            environment.session.user_id = user_id
            raise web.seeother('/pwpolicy')
        else:
            return render.login()