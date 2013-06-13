__author__ = 'zcabh_000'
import web
import hashlib
from environment import render_public as render
from environment import db

class pwrecovery:
    def GET(self, rid):
        res = db.select('pwrecovery', where="rid=$rid&&isrecovered=0", vars=locals())
        if len(res) > 0:
            username = res[0].username
            return render.pwrecovery(username)
        else:
            return "Unknown request"

    def POST(self):
        referer = web.ctx.env.get('HTTP_REFERER', 'http://google.com')
       # return web.ctx.host
        if referer.find(web.ctx.host+'/pwrecovery') >= 0:
            i = web.input()
            password = web.websafe(i.Password)
            username = web.websafe(i.user)
            res = db.update('users', where="username=$username", password=hashlib.sha224(password).hexdigest(), vars=locals())
            if res > 0:
                res = db.update('pwrecovery', where="username=$username", isrecovered=1, vars=locals())
                #return 'Update successful'
                raise web.seeother('/login')
            else:
                return 'Update failed'
        else:
            raise web.seeother('/login')



