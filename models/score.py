__author__ = 'Daniyar'

import itertools
from localsys.storage import db
import math
from sim.simulation import simulation


class score_model:
    def check_closest_competitor(self, usrid, your_score):
        value_risk = 0.0
        value_cost = 0.0
        prev_value_risk = 1.0
        prev_value_cost = 1.0
        next_value_risk = 1.0
        next_value_cost = 1.0
        prev_risk_rank = 0
        next_risk_rank = 0
        prev_cost_rank = 0
        next_cost_rank = 0
        next_value_risk_date = "N/A"
        prev_value_risk_date = "N/A"
        prev_value_cost_date = "N/A"
        next_value_cost_date = "N/A"
        date_risk = "N/A"
        date_cost = "N/A"
        checked = False
        u_rank_risk = 1
        u_rank_cost = 1
        users_risk = []
        users_cost = []
        risk_values = []
        cost_values = []
        scores_1, scores_2 = itertools.tee(your_score)
        for row in scores_1:
            if row.score_type == 1:
                if row.userid == usrid:
                    if not checked:
                        value_risk = row.score_value
                        checked = True
                        date_risk = row.date
                else:
                    if not checked:
                        if not row.userid in users_risk:
                            if not float(row.score_value) in risk_values:
                                users_risk.append(row.userid)
                                risk_values.append(float(row.score_value))
                                u_rank_risk += 1
                                prev_value_risk = row.score_value
                                prev_value_risk_date = row.date
                    else:
                        if not row.userid in users_risk:
                            next_value_risk = row.score_value
                            next_value_risk_date = row.date
                            break
        checked = False
        for row in scores_2:
            if row.score_type == 2:
                if row.userid == usrid:
                    if not checked:
                        value_cost = row.score_value
                        checked = True
                        date_cost = row.date
                else:
                    if not checked:
                        if not row.userid in users_cost:
                            if not float(row.score_value) in cost_values:
                                users_cost.append(row.userid)
                                cost_values.append(float(row.score_value))
                                u_rank_cost += 1
                                prev_value_cost = row.score_value
                                prev_value_cost_date = row.date
                    else:
                        if not row.userid in users_cost:
                            next_value_cost = row.score_value
                            next_value_cost_date = row.date
                            break
        u_rank_risk -= risk_values.count(float(value_risk))
        u_rank_cost -= cost_values.count(float(value_cost))
        prev_risk_rank = u_rank_risk - 1
        if prev_risk_rank == 0:
            prev_value_risk = 9
        prev_cost_rank = u_rank_cost - 1
        if prev_cost_rank == 0:
            prev_value_cost = 9
        if next_value_risk == value_risk:
            next_risk_rank = u_rank_risk
        else:
            next_risk_rank = u_rank_risk + 1
        if next_value_cost == value_cost:
            next_cost_rank = u_rank_cost
        else:
            next_cost_rank = u_rank_cost + 1
        if math.fabs(float(value_risk) - float(prev_value_risk)) <= math.fabs(
                        float(next_value_risk) - float(value_risk)):
            closest_score_risk = prev_value_risk
            closest_ranking_risk = prev_risk_rank
            closest_date_risk = prev_value_risk_date
        else:
            closest_score_risk = next_value_risk
            closest_ranking_risk = next_risk_rank
            closest_date_risk = next_value_risk_date
        if math.fabs(float(value_cost) - float(prev_value_cost)) <= math.fabs(
                        float(next_value_cost) - float(value_cost)):
            closest_score_cost = prev_value_cost
            closest_ranking_cost = prev_cost_rank
            closest_date_cost = prev_value_cost_date
        else:
            closest_score_cost = next_value_cost
            closest_ranking_cost = next_cost_rank
            closest_date_cost = next_value_cost_date

        return value_risk, date_risk, value_cost, date_cost, u_rank_risk, u_rank_cost, closest_score_risk, \
               closest_ranking_risk, closest_date_risk, closest_score_cost, closest_ranking_cost, closest_date_cost

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

    def find_avg(self):
        average_risk = db.query("SELECT AVG(score_value)as avg FROM scores WHERE score_type =1;")[0]
        average_cost = db.query("SELECT AVG(score_value)as avg FROM scores WHERE score_type =2;")[0]
        return average_risk.avg, average_cost.avg

    @classmethod
    def get_scores(cls, id_user):

        all_scores = db.select('scores', order="score_value ASC")
        length = len(all_scores)
        scores_1, scores_2, scores_3, scores_4 = itertools.tee(all_scores, 4)

        if len(all_scores) > 0:
            b_u_risk, b_u_risk_date, b_u_cost, b_u_cost_date, b_u_risk_rank, b_u_cost_rank, c_risk, c_risk_rank, \
            c_risk_when, c_pc, c_pc_rank, c_pc_when = score_model().check_closest_competitor(id_user, scores_2)
            b_risk, b_risk_when, b_pc, b_pc_when = score_model().find_best(scores_3)

            avg_risk, avg_pc = score_model().find_avg()

            msg = {
                "b_u_risk": str(b_u_risk),
                "b_u_risk_date": str(b_u_risk_date),
                "b_u_risk_rank": b_u_risk_rank,
                "b_u_cost": str(b_u_cost),
                "b_u_cost_date": str(b_u_cost_date),
                "b_u_cost_rank": b_u_cost_rank,
                "c_risk": str(c_risk),
                "c_risk_when": str(c_risk_when),
                "c_risk_rank": c_risk_rank,
                "c_pc": str(c_pc),
                "c_pc_when": str(c_pc_when),
                "c_pc_rank": c_pc_rank,
                "b_risk": str(b_risk),
                "b_risk_when": str(b_risk_when),
                "b_pc": str(b_pc),
                "b_pc_when": str(b_pc_when),
                "avg_risk": str(avg_risk),
                "avg_pc": str(avg_pc)
            }
        return msg

    def multiple_score(self, policies):
        policy_costs_risks = []
        sim = simulation()
        for policy_entry in policies:
            result_entry = {}
            for key in policy_entry:
                if key == "data":
                    tmp_value = policy_entry[key]
                    #sim.set_multi_policy(tmp_value)
                    result_entry["risk"] = sim.calc_risk_prob(tmp_value)
                    result_entry["cost"] = sim.calc_prod_cost(tmp_value)
                else:
                    result_entry["id"] = policy_entry[key]
            policy_costs_risks.append(result_entry)

            # print('return cost '+ policy_costs_risks)

        return policy_costs_risks
