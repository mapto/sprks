__author__ = 'Dan'
from environment import render_private as render
import web
import session
from models.policies import policies_model
import json
from environment import render_private as render


class history:
    def GET(self):
        if session.mysession.session.loggedin:
            username = session.mysession.session.user
            user_id = session.mysession.session.id
            date = session.mysession.session.date
            policy_history = policies_model().get_policy_history(user_id)

            if policy_history is not None:
                #return json.dumps(policy_history)
                return render.profile(username, date, policy_history)
            else:
                return "None"
        else:
            raise web.seeother('/home')