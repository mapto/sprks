__author__ = 'Dan'

import json
import web

from localsys.environment import render
from models.users import users_model
from localsys.storage import path
from models.policies import policies_model
from localsys.environment import context

from localsys.storage import db

class history:
    def GET(self):
        if context.user_id() > 0:
            return render.profile()
        else:
            raise web.seeother(path + '/home')


class history_rest:
    def GET(self):
        #get policy history (used in table display on a Profile page)
        policy_history = policies_model.get_policy_history(context.user_id())

        #get risks, costs for all months played by a user (used in graphs display on a Profile page)
        userid = context.user_id()
        scores = db.select('scores', where='userid=$userid', order="date ASC", vars=locals())
        scores_result = []
        for row in scores:
            tmp = {}
            for key, value in row.iteritems():
                tmp[key] = str(value)
            scores_result.append(tmp)
        history = json.dumps(
            {
            'policy_history': json.dumps(policy_history),
            'graph_data': json.dumps(scores_result)
            }
        )

        if history:
            return history