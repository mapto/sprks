"""
OBSOLETE
"""

import json
import web
import localsys
from sim.simulation import simulation
from localsys.storage import db
from localsys.storage import path
from localsys.environment import context
from models.pw_policy import pw_policy_model
from models.score import score_model
from localsys.environment import render


class pwpolicy_rest:

     # the default policy should be specified in a central place and reusable
    default = pw_policy_model.default.copy()
    #    default['date'] = get_start_time().isoformat()

    def GET(self):
        """
        Handles AJAX requests to get client's most recent policies.
        """

        if context.user_id() == 0:
            raise web.seeother(path + '/home')

        check = db.select('pw_policy', where='userid=$context.user_id()', order='date DESC', vars=locals())
        if len(check) > 0:
            result_get = check[0]
            return json.dumps(
                {
                    'plen': result_get.plen,
                    'psets': result_get.psets,
                    'pdict': result_get.pdict,
                    'phist': result_get.phist,
                    'prenew': result_get.prenew,
                    'pattempts': result_get.pattempts,
                    'precovery': result_get.precovery,
                    'date': result_get.date
                }
            )

        else:
            return json.dumps(self.default_policy)
