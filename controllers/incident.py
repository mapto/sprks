__author__ = 'mruskov'

import web
import session
from models.incident import incident as model
from environment import render_private as render
from sim.simulation import simulation
from environment import db
from models.users import users_model


class incident:

    def GET(self):
        if session.mysession.session.loggedin:
            return render.incident(session.mysession.session.user)
        else:
            raise web.seeother('home')

    def POST(self):
        raise web.seeother('score')


class incident_rest:

    def GET(self):
        last_policy = self.get_policy_history(session.mysession.session.user)
        last_policy = last_policy[0]
        incident = simulation().get_related_incidents(last_policy)[0]
        return model.get_incident(incident)['name']

    def get_policy_history(self, id):
        history = db.query('SELECT * FROM pw_policy JOIN users ON userid = Id WHERE username = "' + id + '" ORDER BY date DESC')
#        history = db.select('pw_policy', where="userid=$id", order="date", vars=locals())
        return history