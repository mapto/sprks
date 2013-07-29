__author__ = 'mruskov'

import web
import json
from localsys.environment import render
from localsys.environment import context
from models.incident import incident as model
from localsys.storage import path
from models.policies import policies_model
from sim.simulation import simulation


class incident:

    def GET(self):

        if context.user_id() > 0:  # if a user is logged in
            return render.incident()
        else:
            raise web.seeother(path + '/home')

    def POST(self):
        raise web.seeother(path + '/policy/password')


class incident_rest:

    def GET(self, a='', id=0):
        """
        If given ID, returns dump of incident details.
        """
        if id != 0:
            web.header('Content-Type', 'application/json')
            return json.dumps(model.get_incident(ident=id))

        prev_policies = policies_model.get_policy_history(context.user_id(), latest=True)
        # TODO here taking only the first one. should actually handle all 27 (3x3x3) of them
        # Controllers (and the server as a whole) should not know about the way data is predicted.

        # Regardless how it works, the simulation should appear to the outside as one model that takes a policy and
        # returns an incident

        # This should be a simulation call.
        last_policy = prev_policies[0]
        incident = simulation().get_related_incidents(last_policy)[0]
        return model.get_incident(incident)['name']