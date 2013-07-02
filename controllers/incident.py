__author__ = 'mruskov'

import web
import session
from environment import render_private as render
from models.incident import incident as model

class incident:
    def GET(self):
        name = 'infrequent_use'
        event = model.get_incident(name=name)
        if session.mysession.session.loggedin:
            return render.incident(session.mysession.session.user, event)
        else:
            raise web.seeother('/home')

    def POST(self):
        raise web.seeother('/policy/password')