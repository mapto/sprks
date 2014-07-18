__author__ = 'zhanelya'

import web
import session
from environment import render_private as render
from environment import db
import itertools
import math
from sim.simulation import simulation
import json
from models.policies import policies_model as model
from models.users import users_model

class score:
    def POST(self):
        raise web.seeother('/intro')


    def check_closest_competitor(self, length, usrid, your_score):
        print "entered check closest"
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
        prev_value_risk = 9999
        prev_value_cost = 9999
        next_value_risk = 0.0
        next_value_cost = 0.0
        prev_risk_rank = 0
        next_risk_rank = 0
        prev_cost_rank = 0
        next_cost_rank = 0
        next_value_risk_date = "N/A"
        prev_value_risk_date = "N/A"
        prev_value_cost_date = "N/A"
        next_value_cost_date = "N/A"
        checked = False
        scores_1, scores_2 = itertools.tee(your_score)
        for row in scores_1:
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
                        prev_value_risk_date = row.date
                    else:
                        next_value_risk = row.score_value
                        next_value_risk_date = row.date
                        break
        checked = False
        for row in scores_2:
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
                        prev_value_cost_date = row.date
                    else:
                        next_value_cost = row.score_value
                        next_value_cost_date = row.date
                        break
        print value_risk, prev_value_risk, next_value_risk
        print value_cost, prev_value_cost, next_value_cost
        if next_risk_rank+1 == length:
            next_risk_rank = 0
        if next_cost_rank+1 == length:
            next_cost_rank = 0
        if math.fabs(float(value_risk)-float(prev_value_risk)) <= math.fabs(float(next_value_risk)-float(value_risk)):
            closest_score_risk = prev_value_risk
            closest_ranking_risk = prev_risk_rank
            closest_date_risk = prev_value_risk_date
        else:
            closest_score_risk = next_value_risk
            closest_ranking_risk = next_risk_rank
            closest_date_risk = next_value_risk_date
      #  , ,  = , ,   else , ,
        if math.fabs(float(value_cost)-float(prev_value_cost)) <= math.fabs(float(next_value_cost)-float(value_cost)):
            closest_score_cost = prev_value_cost
            closest_ranking_cost = prev_cost_rank
            closest_date_cost = prev_value_cost_date
        else:
            closest_score_cost = next_value_cost
            closest_ranking_cost = next_cost_rank
            closest_date_cost = next_value_cost_date
        #, ,  = , ,   else , ,

        return closest_score_risk, closest_ranking_risk, closest_date_risk, closest_score_cost, closest_ranking_cost, closest_date_cost

    def find_best_user(self, length, usrid, your_score):
        print "entered find best user"
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
        scores_1, scores_2 = itertools.tee(your_score)
        for row in scores_1:
            if row.score_type == 1:
                if row.userid == usrid:
                    rank_risk += 1
                    date_risk = row.date
                    risk_value = row.score_value
                    break
                else:
                    rank_risk += 1
        for row in scores_2:
            if row.score_type == 2:
                if row.userid == usrid:
                    rank_cost += 1
                    date_cost = row.date
                    cost_value = row.score_value
                    break
                else:
                    rank_cost += 1
        #return b, b_when
        print risk_value, rank_risk, date_risk
        print cost_value, rank_cost, date_cost
        return risk_value, rank_risk, date_risk, cost_value, rank_cost, date_cost

    def find_best(self, scores):
        date_risk = "N/A"
        value_risk = 0.0
        date_cost = "N/A"
        value_cost = 0.0
        scores_1, scores_2 = itertools.tee(scores)
        for row in scores_1:
            if row.score_type == 1:
                date_risk = row.date
                value_risk = row.score_value
                break
        for row in scores_2:
            if row.score_type == 2:
                date_cost = row.date
                value_cost = row.score_value
                break
        return value_risk, date_risk, value_cost, date_cost

    def find_avg(self, your_score):
#        score_type = your_score.score_type

       # average = db.select('scores', where="score_type=$score_type", vars=locals())
        average_risk = db.query("SELECT AVG(score_value)as avg FROM scores WHERE score_type =1;")[0]
        average_cost = db.query("SELECT AVG(score_value)as avg FROM scores WHERE score_type =2;")[0]

        #avg = average[0].avg
        return average_risk.avg, average_cost.avg

    def GET(self):
        #check if is logged in
        if session.mysession.session.loggedin:
            #use this variable to request any ID number
            id_user = session.mysession.session.id

            all_scores = db.select('scores', order="score_value ASC")
            length = len(all_scores)
            scores_1, scores_2, scores_3, scores_4 = itertools.tee(all_scores, 4)
            #your_risk = db.select('scores', where="userid=$id_user and score_type=1", vars=locals())
            #your_pc = db.select('scores', where="userid=$id_user and score_type=2", vars=locals())

            #if user scores found -> display score page

            #if len(your_risk) > 0 and len(your_pc) > 0:
            if len(all_scores) > 0:
                #your_risk = your_risk[0]
                #your_pc = your_pc[0]
                b_u_risk, b_u_risk_rank, b_u_risk_date, b_u_cost, b_u_cost_rank, b_u_cost_date = self.find_best_user(length, id_user, scores_1)
                c_risk, c_risk_rank, c_risk_when, c_pc, c_pc_rank, c_pc_when = self.check_closest_competitor(length, id_user, scores_2)
               # , ,  = self.CHECK_CLOSEST_COMPETITOR(your_pc)
                b_risk, b_risk_when,  b_pc, b_pc_when = self.find_best(scores_3)
              # ,  = self.FIND_BEST(your_pc)
                avg_risk, avg_pc = self.find_avg(scores_4)
                #avg_pc = self.FIND_AVG(your_pc)
                print b_u_risk_rank

                return render.score(session.mysession.session.user,
                                    b_u_risk, b_u_risk_date, b_u_risk_rank,
                                    b_u_cost, b_u_cost_date, b_u_cost_rank,
                                    c_risk, c_risk_when, c_risk_rank,
                                    c_pc, c_pc_when, c_pc_rank,
                                    b_risk, b_risk_when,
                                    b_pc, b_pc_when,
                                    avg_risk,
                                    avg_pc, session.mysession.session.date)


            else:
                #if user scores not found -> assume that no term has been finished yet
                return 'You have not finished any term yet'
        else:
            #if user not logged in -> redirect to login page
            raise web.seeother('/home')


class multiple_score:
    def POST(self):
        web.header('Content-Type', 'application/json')
        sim = simulation()
        post_data = json.loads(web.data())
        policy_costs_risks = []

        last_policy = model().get_policy_history(session.mysession.session.user)
        for policy_entry in post_data:
            result_entry = {}
            for key, value in policy_entry.iteritems():
                if key == "data":
                    next_policy = json.loads(value)
                else:
                    result_entry[key] = value
            result_entry["risk"] = sim.get_risk(next_policy)
            result_entry["cost"] = sim.calc_prod_cost(next_policy)
            policy_costs_risks.append(result_entry)

        # print('return cost '+ policy_costs_risks)

        return json.dumps(policy_costs_risks)

