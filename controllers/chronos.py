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

        sync_date = self.sync_history(context.user_id(), client_date, payload.get('newCosts'))

        if client_date.day == 1:
            pass
            # payload.get('policyUpdate')

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

    def sync_history(self, user_id, client_date, new_costs):
        # Synchronizes history where possible, and returns the date that the client should resume at.
        last_sync_date = records.last_sync(user_id)
        if client_date <= last_sync_date:
            return last_sync_date
        else:
            # The client is ahead of the server date.

            #query SELECT * FROM journal WHERE user_id=user_id AND committed=false AND date<$date GROUP BY date ORDER BY date
            # if rows > 1: an eventful day was missed - backtrack to the previous day

            # if any events were skipped, go to the day of the first missed event

            # if policy update was skipped
            # go back to previous day


            if not records.validate_journal(context.user_id(), date, new_costs):
                pass
                # newCosts dont match - log an error
