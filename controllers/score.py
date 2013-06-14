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
            your_risk = db.select('scores', where="userid=$id_user and score_type=1", vars=locals())

            your_pc = db.select('scores', where="userid=$id_user and score_type=2", vars=locals())
            #closest_risk =
            #closest_pc =
            if len(your_risk) > 0 and len(your_pc) > 0:
                result_y_risk = your_risk[0]
                result_y_pc = your_pc[0]
                return render.score(result_y_risk.score_value, result_y_risk.date, result_y_risk.rank,
                                    result_y_pc.score_value, result_y_pc.date, result_y_pc.rank)
            else:
                return 'not found'
        else:
            raise web.seeother('/login')