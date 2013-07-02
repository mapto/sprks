__author__ = 'mruskov'

import web
from localsys.environment import render
from localsys.environment import context


class intro:
    def GET(self):
        if context.user_id() > 0:
            return render.intro()
        else:
            raise web.seeother('/home')

    def POST(self):
        raise web.seeother('/policy/password')
