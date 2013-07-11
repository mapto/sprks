import json
import web
import localsys
from datetime import date
from localsys.environment import context
import models
from libraries.utils import date_utils
from models.policies import policies_model
from models.journal import records


class chronos:

    def POST(self):
        """
        Listens to POST requests for main Chronos API
        """

        payload = json.loads(web.data())
        web.header('Content-Type', 'application/json')

        client_date = date_utils.iso8601_to_date(payload.get('date', '2014-01-06'))

        if context.user_id() == 0:
            return json.dumps({
                'success': False,
                'messages': ['Unauthorized']
            })



        sync_date = records.sync_history(context.user_id(), client_date)

        policy_update = payload.get('policyUpdate')

        updated_policy = {}

        if policy_update is not None:
            updated_policy = policies_model().parse_policy()
            latest_policy = policies_model().iter_to_nested_obj(policies_model().get_latest_policy(context.user_id()))
            merged_policy = policies_model().merge_policies(updated_policy, latest_policy)
            print policies_model().nested_obj_to_list_of_dict(merged_policy)

        if sync_date.day == 1 and policy_update is not None:
            for policy_change in policy_update.iteritems():
                policy_change

            # delete old prophecy
            # self.prophesize()
            # add new prophecy to journal


        # calendar = get current month from journal
        response = {
                'date': sync_date.isoformat(),
                'policyAccept': True,
                'interventionAccept': True,
                'calendar': [
                    {
                        # calendar
                    }
                ]
        }
        if not payload.get('silentMode', False):
            response = {
                'date': '2013-02-06',
                'policyAccept': True,
                'interventionAccept': True,
                'calendar': [
                    {
                        # calendar
                    }
                ],
                'policy': [
                    {
                        'employee': 'executive',
                        'location': 'home',
                        'device': 'mobile',
                        'plen': 8,
                        'psets': 2,
                        'pdict': 0,
                        'phist': 1,
                        'prenew': 1,
                        'pattempts': 0,
                        'precovery': 1
                    }
                        ]
            }
       # if payload.get('initPolicy', False):
                # get user's policy data
                #response['policy'] = policies_model.get_policy_history(context.user_id(), latest=True)

            #return json.dumps(response)

        return json.dumps(response)


