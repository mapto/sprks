__author__ = 'zcabh_000'
from web import form
import web
import hashlib
import session

render = web.template.render('C:/Users/zcabh_000/PycharmProjects/sprks/templates/')


class login:
    def GET(self):
        #login = form.Form(
         #   form.Textbox('username'),
          #  form.Password('password'),
           # form.Button('Login'),
            #form.Radio('radio', ['Radio', 'R']), )
       # f = login()
        #return f.render()
        session.mysession.session.loggedin=False
        session.mysession.session.user='Anonimous'
        return render.login()

    def POST(self):
        i = web.input()
        usrname = i.username
        password = hashlib.sha224(i.password).hexdigest()
        db = web.database(dbn='mysql', user='root', pw='12345', db='sprks')
        id_tmp = db.select('users', where="username=$usrname&&password=$password", vars=locals())
        if len(id_tmp) > 0:
            session.mysession.session.loggedin=True
            session.mysession.session.user=usrname
            raise web.seeother('/secured_page')
        else:
            return render.login()





