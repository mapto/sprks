import json
import web
import localsys
from datetime import date
from localsys.environment import context
import models


class chronos:

    def POST(self):
        """
        Listens to POST requests for main Chronos API
        """

        payload = json.loads(web.data())
        web.header('Content-Type', 'application/json')

        if context.user_id() == 0:
            return json.dumps({
                'success': False,
                'messages': ['Unauthorized']
            })

        sync_date = self.sync_history(payload.get('date'), payload.get('newCosts'))


        #if monthly sync or event sync

            # if date is first day of month
                # payload.get('policyUpdate')

            # if event occured on the previous day
                # payload.get('intervention')

            # delete old prophecy
            # self.prophesize()
            # add new prophecy to journal

        # calendar = get current month from journal

        if not payload.get('silentMode', False):
            response = {

                'date': date(2000, 1, 1).isoformat(),
                'policyAccept': True,
                'interventionAccept': True,
                'calendar': [
                    {
                        # calendar
                    }
                ]
            }

            if payload.get('initPolicy', False):
                # get user's policy data
                response['policy'] = models.policies.policies_model.get_latest_policy(context.user_id())

            return json.dumps(response)

    def sync_history(self, date, new_costs):
        # look for past uncommitted interventions that haven't been handled
        # if client is behind, make it catch up. if client is ahead, throw error at the date they should backtrack
        # Synchronizes history where possible, and returns the date that the client to resume at.
        pass

    def prophesize(self):
        """
        Generates calendar of future events.
        """
        pass