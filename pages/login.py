__author__ = 'zcabh_000'

import web
import hashlib
import session
from settings import settings


class login:
    '''Views (as in MVC pattern) commonly need a reference to the model (db) and also templates
       These are declared as class attributes
    '''
    render = settings().render
    db = settings().db

    def GET(self):
        session.mysession.session.loggedin=False
        session.mysession.session.user='Anonimous'
        return self.render.login()

    def POST(self):
        i = web.input()
        usrname = i.username
        password = hashlib.sha224(i.password).hexdigest()
        id_tmp = self.db.select('users', where="username=$usrname&&password=$password", vars=locals())
        if len(id_tmp) > 0:
            session.mysession.session.loggedin=True
            session.mysession.session.user=usrname
            session.mysession.session.id=id_tmp[0].Id
            raise web.seeother('/pwpolicy')
        else:
            return self.render.login()





