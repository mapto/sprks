__author__ = 'zcabh_000'
import web
import hashlib
import session

render = web.template.render('C:/Users/zcabh_000/PycharmProjects/sprks/templates/')


class register:
    def GET(self):
        return render.register()
    def POST(self):
        """
        Stores user details into 'users' table. Password is encrypted using sha224 algorithm

        """
        db = web.database(dbn='mysql', user='root', pw='12345', db='sprks')
        i = web.input()
        usrname = i.username
        tmp = db.select('users', where="username=$usrname", vars=locals())
        if len(tmp) > 0:
            return render.register("User already exists")
        id = db.insert('users', username=i.username, email=i.email, password=hashlib.sha224(i.password).hexdigest())
        raise web.seeother('/login')