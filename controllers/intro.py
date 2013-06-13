__author__ = 'mruskov'

import web
import session
from environment import render_private as render


class intro:
    def GET(self):
        if session.mysession.session.loggedin:
            return render.intro()
        else:
            raise web.seeother('/login')

    def POST(self):
        raise web.seeother('/pwpolicy')