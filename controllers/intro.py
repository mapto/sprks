__author__ = 'mruskov'

import web
import session
from environment import render_private as render


class intro:
    def GET(self):
        if session.mysession.session.loggedin:
            return render.intro(session.mysession.session.user, session.mysession.session.turn)
        else:
            raise web.seeother('/home')

    def POST(self):
#        session.mysession.session.user
        raise web.seeother('/policy')