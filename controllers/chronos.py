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
        client_date = date_utils.iso8601_to_date(payload.get('date'))

        if context.user_id() == 0:
            return json.dumps({
                'success': False,
                'messages': ['Unauthorized']
            })

        sync_date = self.sync_history(client_date, payload.get('newCosts'))

        if client_date.day == 1:
            pass
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
                response['policy'] = policies_model.get_latest_policy(context.user_id())

            return json.dumps(response)

    def sync_history(self, date, new_costs):
        query = 'SELECT * FROM journal WHERE committed=false AND date<date GROUP BY date'
        #if result.length == 1
        # if client is behind, make it catch up. if client is ahead, throw error at the date they should backtrack
        # Synchronizes history where possible, and returns the date that the client to resume at.
        records.validate_journal(context.user_id(), date, new_costs)

    def prophesize(self):
        """
        Generates calendar of future events.
        """
        pass