__author__ = 'ZHANELYA'

import json
import web
from models.gtd import goal_task_differentiation as gtd
from localsys.environment import context
from models.policies import policies_model
from localsys.storage import db

class report:
    def POST(self):
        payload = json.loads(web.data())
        employees_number = payload['employees_number']
        gtd_instance = gtd(context.user_id())
        risk_cost = gtd_instance.get_goal_task_differentiation(employees_number)

        report = {"policy":[], "employees":[], "total":{}}
        report['policy'] = policies_model.get_policies_list(context.user_id())
        report['employees'] = risk_cost['employees']
        report['total'] = risk_cost['total']
        return json.dumps(report)
