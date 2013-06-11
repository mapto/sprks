__author__ = 'zcabh_000'
import web
import hashlib
from settings import settings


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
        raise web.seeother('/login')