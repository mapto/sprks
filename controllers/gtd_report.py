__author__ = 'ZHANELYA'

import json
from models.gtd import goal_task_differentiation as gtd
from localsys.environment import context
from models.policies import policies_model

class report:
    def GET(self):
        #gtd.get_goal_task_differentiation(context.user_id())
        report = {"policy":[], "employees":[], "total":{}}

        report['policy'] = policies_model.get_policies_list(context.user_id())

        empl_positions = [ 'padh', 'som', 'bdd',
                  'cam', 'rm', 'pm',
                  'ft', 'sc', 'sm']
        employees = []
        for i in range(len(empl_positions)):
            report['employees'].append({"employee":empl_positions[i],"risk":i*0.01,"p_cost":i*0.05})

        report['total']['risk'] = 0.8
        report['total']['p_cost'] = 0.9

        return json.dumps(report)