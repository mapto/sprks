__author__ = 'mruskov'

import web
import session
from environment import render_private as render


class intro:
    def GET(self):
        if session.mysession.session.loggedin:
            return render.intro(session.mysession.session.user)
        else:
            raise web.seeother('/home')

    def POST(self):
        raise web.seeother('/pwpolicy')