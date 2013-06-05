__author__ = 'zcabh_000'
import session
import web

render = web.template.render('C:/Users/zcabh_000/PycharmProjects/sprks/templates/')


class secured_page:
    def GET(self):
        if session.mysession.session.loggedin:
            return render.secured_page(session.mysession.session.user)
        else:
            raise web.seeother('/login')
