import session
import web
from settings_prelogin import settings


class secured_page:
    def GET(self):
        render = settings().render
        if session.mysession.session.loggedin:
            return render.secured_page(session.mysession.session.user)
        else:
            raise web.seeother('/login')
