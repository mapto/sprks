__author__ = 'zcabh_000'
from web import form
import web


class login:
    def GET(self):
        login = form.Form(
            form.Textbox('username'),
            form.Password('password'),
            form.Button('Login'),
            form.Radio('radio', ['Radio', 'R']), )
        f = login()
        return f.render()

    def POST(self):
        i = web.input()
        db = web.database(dbn='mysql', user='root', pw='12345', db='sprks')
        id = db.insert('pw_policy', plen=3, psets=3, pdict=1, psim='test', prenew='monthly', pattempts=2, precovery='manned')
        if id > 0:
            return 'OK'





