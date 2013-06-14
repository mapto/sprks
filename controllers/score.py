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

            if len(your_risk) > 0 and len(your_pc) > 0:
                your_risk = your_risk[0]
                your_pc = your_pc[0]

                c_risk = your_risk.score_value
                c_risk_when = your_risk.date
                c_risk_rank = your_risk.rank
                c_pc = your_pc.score_value
                c_pc_when = your_pc.date
                c_pc_rank = your_pc.rank

                rank = your_risk.rank

                closest_risk = db.select('scores', where="score_type=1 and rank=$rank-1", vars=locals())
                if len(closest_risk) > 0:
                    closest_risk=closest_risk[0]

                    #update closest values if a closest RISK competitor is found
                    c_risk = closest_risk.score_value
                    c_risk_when = closest_risk.date
                    c_risk_rank = closest_risk.rank

                closest_pc = db.select('scores', where="score_type=2 and rank=$rank-1", vars=locals())
                if len(closest_pc) > 0:
                    closest_pc=closest_pc[0]

                    #update closest values if a closest ProdCOST competitor is found
                    c_pc = closest_pc.score_value
                    c_pc_when = closest_pc.date
                    c_pc_rank = closest_pc.rank

                return render.score(your_risk.score_value, your_risk.date, your_risk.rank,
                                    your_pc.score_value, your_pc.date, your_pc.rank,
                                    c_risk, c_risk_when, c_risk_rank,
                                    c_pc, c_pc_when, c_pc_rank)
            else:
                return 'You have not finished any term yet'
        else:
            raise web.seeother('/login')