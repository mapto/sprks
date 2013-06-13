__author__ = 'zhanelya'

import web
import session
from environment import render_private as render
from environment import db

class score:
    def GET(self):
        if session.mysession.session.loggedin:
            #use this variable to request any ID number
            id_user = session.mysession.session.id
            check = db.select('scores', vars=locals())
            if len(check) > 0:
                result_get = check[0]
                return render.score(8,2,3,result_get.prob, result_get.impact, result_get.cost)
            else:
                return 'not found'
        else:
            raise web.seeother('/login')