__author__ = 'ZHANELYA'

import json
from models.gtd import goal_task_differentiation as gtd
# from models.gtd.goal_task_differentiation import get_goal_task_differentiation as gtd
from localsys.environment import context
from models.policies import policies_model
#from gtd.

class report:
    def GET(self):
        gtd_instance = gtd(context.user_id())
        risk_cost = gtd_instance.get_goal_task_differentiation()

        report = {"policy":[], "employees":[], "total":{}}
        report['policy'] = policies_model.get_policies_list(context.user_id())
        report['employees'] = risk_cost['employees']
        report['total'] = risk_cost['total']
        return json.dumps(report)
