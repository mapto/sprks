__author__ = 'mruskov'

import web
from localsys.environment import render
from localsys.environment import context
from localsys.storage import path


class intro:
    def GET(self):
        if context.user_id() > 0:
            return render.intro()
        else:
            raise web.seeother(path + '/home')

    def POST(self):
        raise web.seeother(path + '/policy/password')
