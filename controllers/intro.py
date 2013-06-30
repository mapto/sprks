__author__ = 'mruskov'

import web
import environment
from environment import render_private as render
from models.users import users_model


class intro:
    def GET(self):
        if environment.session.user_id > 0:
            return render.intro(users_model().get_username(environment.session.user_id))
        else:
            raise web.seeother('/home')

    def POST(self):
        raise web.seeother('/pwpolicy')