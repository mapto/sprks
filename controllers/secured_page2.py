__author__ = 'zcabh_000'
import session
import web
from environment import render_private as render


class secured_page:
    def GET(self):
        if session.mysession.session.loggedin:
            return render.secured_page2(session.mysession.session.user)
        else:
            raise web.seeother('/login')