__author__ = 'mruskov'

import web
from localsys.environment import render
from models.users import users_model


class intro:
    def GET(self):
        if users_model.authorize() > 0:
            return render.intro()
        else:
            raise web.seeother('/home')

    def POST(self):
        raise web.seeother('/policy/password')
