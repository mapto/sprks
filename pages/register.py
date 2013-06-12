__author__ = 'zcabh_000'
import web
import hashlib
from settings import settings
import session


class register:
    profile = settings()
    render = profile.render
    db = profile.db

    def GET(self):
        return self.render.register()
    def POST(self):
        """
        Stores user details into 'users' table. Password is encrypted using sha224 algorithm

        """
        i = web.input()
        usrname = i.username
        tmp = self.db.select('users', where="username=$usrname", vars=locals())
        if len(tmp) > 0:
            return self.render.register("User already exists")
        id = self.db.insert('users', username=i.username, email=i.email, password=hashlib.sha224(i.password).hexdigest())
        id_tmp = self.db.select('users', where="username=$usrname", vars=locals())
        if len(id_tmp) > 0:
            session.mysession.session.loggedin=True
            session.mysession.session.user=usrname
            session.mysession.session.id=id_tmp[0].Id
            raise web.seeother('/pwpolicy')
        else:
            return self.render.login()