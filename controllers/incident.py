__author__ = 'mruskov'

import web
import json
from localsys.environment import render
from localsys.environment import context
from models.incident import incident as model
from localsys.storage import path
from models.policies import policies_model
from sim.simulation import simulation
from models.simulation import simulation as sim_model


class incident_rest:

    def GET(self, a='', id=0):
        """
        If given ID, returns dump of incident details.
        TODO: Should probably return also incident context (employee, location, ...) details
        """
        if id != 0:
            web.header('Content-Type', 'application/json')
            return json.dumps(model.get_incident(ident=id))

        prev_policies = policies_model.get_policy_history(context.user_id(), latest=True)
        # Controllers (and the server as a whole) should not know about the way data is predicted.

        # Regardless how it works, the simulation should appear to the outside
        # as one model that takes a policy and returns an incident

        for policy in prev_policies:
            policy_context = {
                "employees": [policy['employee']],
                "locations": [policy['location']],
                "devices":[policy['device']]}
            related = sim_model().request(policy, policy_context)
            max = model.get_most_probable(related)
        return max['name']
