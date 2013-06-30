__author__ = 'mruskov'

import web
import localsys
from localsys.environment import render
from models.users import users_model
from libraries.user_helper import auth


class intro:
    def GET(self):
        if auth().check() > 0:
            return render.intro()
        else:
            raise web.seeother('/home')

    def POST(self):
        raise web.seeother('/pwpolicy')