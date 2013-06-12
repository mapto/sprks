__author__ = 'zcabh_000'

import web
import session
from settings import settings
from models.users import users_model


class login:
    """ Controllers commonly need a reference to the model (db) and also views
       These are declared as class attributes
    """
    render = settings().render
    db = settings().db

    def GET(self):
        session.mysession.session.loggedin=False
        session.mysession.session.user='Anonymous'
        return self.render.login()

    def POST(self):
        request = web.data()
        auth = users_model().authenticate(request.username, request.password)
        if len(auth) == 1:
            session.mysession.session.loggedin=True
            session.mysession.session.user=request.username
            session.mysession.session.id=auth[0].Id
            raise web.seeother('/pwpolicy')
        else:
            return self.render.login()





