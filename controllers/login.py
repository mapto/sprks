
__author__ = "Dan"

import web
import session
from environment import render_public as render
from models.users import users_model


class login:
    """ Controllers commonly need a reference to the model (db) and also views
       These are declared in environment
    """

    def GET(self):
        session.mysession.session.loggedin = False
        session.mysession.session.user = 'Anonymous'
        session.mysession.session.date = ""
        session.mysession.session.turn = 0
        return render.login()

    def POST(self):
        request = web.input()
        user_id = users_model().authenticate(request.username, request.password)
        if user_id > 0:
            session.mysession.session.loggedin = True
            session.mysession.session.user = request.username
            session.mysession.session.id = user_id
            session.mysession.session.turn = users_model().get_turn(request.username)
            raise web.seeother('/intro')
        else:
            return render.login()