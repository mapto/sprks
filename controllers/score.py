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

    def FIND_BEST(self, your_score):
        score_type = your_score.score_type

        best = db.select('scores', where="score_type=$score_type and rank=1", vars=locals())[0]

        b = best.score_value
        b_when = best.date
        return b, b_when

    def FIND_AVG(self, your_score):
        score_type = your_score.score_type

       # average = db.select('scores', where="score_type=$score_type", vars=locals())
        average = db.query("SELECT AVG(score_value)as avg FROM scores WHERE score_type ="+"$score_type;", vars=locals())

        avg = average[0].avg
        return avg


    def GET(self):
        #check if is logged in
        if session.mysession.session.loggedin:
            #use this variable to request any ID number
            id_user = session.mysession.session.id

            your_risk = db.select('scores', where="userid=$id_user and score_type=1", vars=locals())
            your_pc = db.select('scores', where="userid=$id_user and score_type=2", vars=locals())

            #if user scores found -> display score page
            if len(your_risk) > 0 and len(your_pc) > 0:
                your_risk = your_risk[0]
                your_pc = your_pc[0]

                c_risk, c_risk_when, c_risk_rank = self.CHECK_CLOSEST_COMPETITOR(your_risk)
                c_pc, c_pc_when, c_pc_rank = self.CHECK_CLOSEST_COMPETITOR(your_pc)
                b_risk, b_risk_when = self.FIND_BEST(your_risk)
                b_pc, b_pc_when = self.FIND_BEST(your_pc)
                avg_risk = self.FIND_AVG(your_risk)
                avg_pc = self.FIND_AVG(your_pc)

                return render.score(your_risk.score_value, your_risk.date, your_risk.rank,
                                    your_pc.score_value, your_pc.date, your_pc.rank,
                                    c_risk, c_risk_when, c_risk_rank,
                                    c_pc, c_pc_when, c_pc_rank,
                                    b_risk, b_risk_when,
                                    b_pc, b_pc_when,
                                    avg_risk,
                                    avg_pc)


            else:
                #if user scores not found -> assume that no term has been finished yet
                return 'You have not finished any term yet'
        else:
            #if user not logged in -> redirect to login page
            raise web.seeother('/login')
