__author__ = 'zcabh_000'

import web
import hashlib
import session

render = web.template.render('C:/Users/zcabh_000/PycharmProjects/sprks/templates/')


class login:
    def GET(self):
        session.mysession.session.loggedin=False
        session.mysession.session.user='Anonimous'
        return render.login()

    def POST(self):
        i = web.input()
        usrname = i.username
        password = hashlib.sha224(i.password).hexdigest()
        db = web.database(dbn='mysql', user='root', pw='1234', db='sprks')
        id_tmp = db.select('users', where="username=$usrname&&password=$password", vars=locals())
        if len(id_tmp) > 0:
            session.mysession.session.loggedin=True
            session.mysession.session.user=usrname
            session.mysession.session.id=id_tmp[0].Id
            raise web.seeother('/pwpolicy')
        else:
            return render.login()





