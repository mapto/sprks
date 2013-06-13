import session
import web
from environment import render_private as render

class secured_page:
    def GET(self):
        if session.mysession.session.loggedin:
            return render.secured_page(session.mysession.session.user)
        else:
            raise web.seeother('/login')
