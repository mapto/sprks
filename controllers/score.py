__author__ = 'zhanelya'

import web
import session
from environment import render_private as render
from environment import db

class score:
    def CHECK_CLOSEST_COMPETITOR(self, usrid, your_score):
        """c = your_score.score_value
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
                    c_rank = closest.rank"""
        value_risk = 0.0
        value_cost = 0.0
        prev_value_risk = 0.0
        prev_value_cost = 0.0
        next_value_risk = 0.0
        next_value_cost = 0.0
        prev_risk_rank = 0
        next_risk_rank = 0
        prev_cost_rank = 0
        next_cost_rank = 0
        checked = False
        for row in your_score:
            if row.score_type == 1:
                if row.userid == usrid:
                    next_risk_rank += 1
                    if not checked:
                        value_risk = row.score_value
                        checked = True
                else:
                    next_risk_rank += 1
                    if not checked:
                        prev_risk_rank += 1
                        prev_value_risk = row.score_value
                        prev_value_risk_date = row.date_time
                    else:
                        next_value_risk = row.score_value
                        next_value_risk_date = row.date_time
                        break
        checked = False
        for row in your_score:
            if row.score_type == 2:
                if row.userid == usrid:
                    next_cost_rank += 1
                    if not checked:
                        value_cost = row.score_value
                        checked = True
                else:
                    next_cost_rank += 1
                    if not checked:
                        prev_cost_rank += 1
                        prev_value_cost = row.score_value
                        prev_value_cost_date = row.date_time
                    else:
                        next_value_cost = row.score_value
                        next_value_cost_date = row.date_time
                        break
        closest_score_risk, closest_ranking_risk, closest_date_risk = prev_value_risk, prev_risk_rank, prev_value_risk_date if abs(value_risk-prev_value_risk) < abs(next_value_risk-value_risk) else next_value_risk, next_risk_rank, next_value_risk_date
        closest_score_cost, closest_ranking_cost, closest_date_cost = prev_value_cost, prev_cost_rank, prev_value_cost_date if abs(value_cost-prev_value_cost) < abs(next_value_cost-value_cost) else next_value_cost, next_cost_rank, next_value_cost_date
        return closest_score_risk, closest_ranking_risk, closest_date_risk, closest_score_cost, closest_ranking_cost, closest_date_cost

    def FIND_BEST_USER(self, usrid, your_score):
        """score_type = your_score.score_type

        best = db.select('scores', where="score_type=$score_type and rank=1", vars=locals())[0]

        b = best.score_value
        b_when = best.date"""

        rank_risk = 0
        rank_cost = 0
        date_risk = "N/A"
        date_cost = "N/A"
        risk_value = 0.0
        cost_value = 0.0
        for row in your_score:
            if row.score_type == 1:
                if row.userid == usrid:
                    rank_risk += 1
                    date_risk = row.date_time
                    risk_value = row.score_value
                    break
                else:
                    rank_risk += 1
        for row in your_score:
            if row.score_type == 2:
                if row.userid == usrid:
                    rank_cost += 1
                    date_cost = row.date_time
                    cost_value = row.score_value
                    break
                else:
                    rank_cost += 1
        #return b, b_when
        return risk_value, rank_risk, date_risk, cost_value, rank_cost, date_cost

    def FIND_BEST(self, scores):
        date_risk = "N/A"
        value_risk = 0.0
        date_cost = "N/A"
        value_cost = 0.0
        for row in scores:
            if row.score_type == 1:
                date_risk = row.date_time
                value_risk = row.score_value
                break
        for row in scores:
            if row.score_type == 2:
                date_cost = row.date_time
                value_cost = row.score_value
                break
        return value_risk, date_risk, value_cost, date_cost

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

            all_scores = db.select('scores', order="score_value ASC")

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
