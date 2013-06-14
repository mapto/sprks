__author__ = 'zhanelya'

import web
import session
from environment import render_private as render
from environment import db

class score:
    def CHECK_CLOSEST_COMPETITOR(self, your_score):
        c = your_score.score_value
        c_when = your_score.date
        c_rank = your_score.rank

        rank=your_score.rank
        score_type = your_score.score_type

        closest = db.select('scores', where="score_type=$score_type and rank=$rank-1", vars=locals())
        if len(closest) > 0:
                    closest = closest[0]

                    #update closest values if a closest competitor for this score type is found
                    c = closest.score_value
                    c_when = closest.date
                    c_rank = closest.rank
        return c, c_when, c_rank

    def GET(self):
        if session.mysession.session.loggedin:
            #use this variable to request any ID number
            id_user = session.mysession.session.id

            your_risk = db.select('scores', where="userid=$id_user and score_type=1", vars=locals())
            your_pc = db.select('scores', where="userid=$id_user and score_type=2", vars=locals())

            if len(your_risk) > 0 and len(your_pc) > 0:
                your_risk = your_risk[0]
                your_pc = your_pc[0]

                c_risk, c_risk_when, c_risk_rank = self.CHECK_CLOSEST_COMPETITOR(your_risk)
                c_pc, c_pc_when, c_pc_rank = self.CHECK_CLOSEST_COMPETITOR(your_pc)


                return render.score(your_risk.score_value, your_risk.date, your_risk.rank,
                                    your_pc.score_value, your_pc.date, your_pc.rank,
                                    c_risk, c_risk_when, c_risk_rank,
                                    c_pc, c_pc_when, c_pc_rank)


            else:
                return 'You have not finished any term yet'
        else:
            raise web.seeother('/login')
