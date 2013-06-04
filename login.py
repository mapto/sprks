__author__ = 'zcabh_000'
from web import form
import web
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
        return render.login()

    def POST(self):
        i = web.input()
        db = web.database(dbn='mysql', user='root', pw='12345', db='sprks')
        id = db.insert('pw_policy', plen=i.plen, psets=i.psets, pdict=i.pdict, psim=i.psim, prenew=i.prenew,
                       pattempts=i.pattempts, precovery=i.precovery)
        if id > 0:
            return render.test()





