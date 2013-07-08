__author__ = 'Dan'

import json
import web

from localsys.environment import render
from models.users import users_model
import localsys
from models.policies import policies_model
from localsys.environment import context

class history:
    def GET(self):
        if context.user_id() > 0:
            return render.profile()
        else:
            raise web.seeother('/home')

class history_rest:
    def GET(self):
        policy_history = policies_model().get_policy_history(context.user_id())
        if policy_history:
            return json.dumps(policy_history)