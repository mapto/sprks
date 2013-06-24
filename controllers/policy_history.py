__author__ = 'Dan'
from environment import render_private as render
import web
import session
from models.users import users_model
import json

class history:
    def GET(self):
        if session.mysession.session.loggedin:
            user_id = session.mysession.session.id
            policy_history = users_model().get_policy_history(user_id)
            if policy_history is not None:
                return json.dumps(policy_history)
            else:
                return "None"
        else:
            raise web.seeother('/home')