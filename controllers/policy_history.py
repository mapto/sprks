__author__ = 'Dan'

import json
import web

from models.policies import policies_model
from localsys.environment import context
from localsys.storage import db


class history_rest:
    def GET(self):

        web.header('Content-Type', 'application/json')

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


class score_frame:
    """
    Provides data for a risk and cost scores in the bottom left corner
    (different from the score page as the latter takes only best values)
    Is similar to graph_data for the profile page
    """
    def GET(self):
        # get the latest risk and cost

        user_id = context.user_id()
        web.header('Content-Type', 'application/json')
        scores = db.select('scores', where='userid=$user_id', order="date DESC", limit=2, vars=locals())
        scores_result = []
        for row in scores:
            tmp = {}
            for key, value in row.iteritems():
                tmp[key] = str(value)
            scores_result.append(tmp)

        return json.dumps(scores_result)