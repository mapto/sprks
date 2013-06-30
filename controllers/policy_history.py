__author__ = 'Dan'

import json

import web

from environment import render_private as render
from models.users import users_model
import environment
from models.policies import policies_model


class history:
    def GET(self):
        if environment.session.user_id > 0:
            user_id = environment.session.user_id
            username = users_model.get_username(user_id)
            date = environment.session.date
            policy_history = policies_model().get_policy_history(user_id)

            if policy_history:
                print json.dumps(policy_history)
                return render.profile(username, date, policy_history)
            else:
                return "None"
        else:
            raise web.seeother('/home')