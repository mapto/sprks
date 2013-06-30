__author__ = 'Dan'

import json

import web

from localsys.environment import render
from models.users import users_model
import localsys
from models.policies import policies_model
from libraries.user_helper import auth


class history:
    def GET(self):
        user_id = auth().check()
        if user_id > 0:
            username = users_model().get_username(user_id)
            date = localsys.storage.session.date
            policy_history = policies_model().get_policy_history(user_id)

            if policy_history:
                print json.dumps(policy_history)
                return render.profile(username, date, policy_history)
            else:
                return "None"
        else:
            raise web.seeother('/home')