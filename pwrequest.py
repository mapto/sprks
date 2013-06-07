__author__ = 'zcabh_000'
import random
import web
import hashlib
import os

render = web.template.render('C:/Users/zcabh_000/PycharmProjects/sprks/templates/')


class pwrequest:
    def GET(self):
        return render.pwrequest()

    def POST(self):
        username = web.input().Username
        db = web.database(dbn='mysql', user='root', pw='12345', db='sprks')
        id_tmp = db.select('users', where="username=$username", vars=locals())
        if len(id_tmp) > 0:
            emailaddr = id_tmp[0].email
            random.seed()
            rid = hashlib.sha224(username+str(random.randint(1233, 123455))).hexdigest()
            web.config.smtp_server = 'smtp.gmail.com'
            web.config.smtp_port = 587
            web.config.smtp_username = 'sprkssuprt@gmail.com'
            web.config.smtp_password = 'sprks123456789'
            web.config.smtp_starttls = True
            tmp = db.insert('pwrecovery', username=username, date=web.SQLLiteral('NOW()'), rid=rid, isrecovered=0)
            web.sendmail('support', emailaddr, 'Password recovery', 'http://localhost:8080/pwrecovery/'+rid)
            return "Email is sent"
        else:
            return "User is not found!"
