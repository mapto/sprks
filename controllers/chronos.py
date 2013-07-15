import json
import web
from localsys.environment import context
from libraries.utils import date_utils
from models.policies import policies_model
from models.journal import records
from datetime import timedelta
from models.oracle import prophet


class chronos:

    def POST(self):
        """
        Listens to POST requests for main Chronos API
        """

        payload = json.loads(web.data())
        web.header('Content-Type', 'application/json')

        event_accept = False
        policy_accept = False

        client_date = date_utils.iso8601_to_date(payload.get('date', '2014-01-06'))

        if context.user_id() == 0:
            return json.dumps({
                'success': False,
                'messages': ['Unauthorized']
            })

        # corrected_sync_date backtracks if client submits invalid date.
        corrected_sync_date = records.sync_history(context.user_id(), client_date)

        policy_update = payload.get('policyUpdate')

        if corrected_sync_date.day == 1:
            if policy_update is None:
                # Expecting a policy update, but not found.
                corrected_sync_date -= timedelta(days=1)
            else:
                policies_model.commit_policy_update(policy_update, corrected_sync_date)
                policy_accept = True

        # TODO next_due_event_date shouldn't be called again - convert from @classmethod?
        if corrected_sync_date == records.next_due_event_date(context.user_id()):
            event_accept = True

        if event_accept or policy_accept:
            records.clear_prophecy(context.user_id(), corrected_sync_date)
            prophecy = prophet.prophesize(context.user_id(), corrected_sync_date)
            records.record_prophecy(context.user_id(), prophecy)

        response = {
            'date': corrected_sync_date.isoformat(),
            'policyAccept': policy_accept,
            'eventAccept': event_accept,
            'calendar': [
                records.get_calendar(context.user_id(), corrected_sync_date)
            ]
        }

        if payload.get('initPolicy', False):
            response['policy'] = policies_model().get_policies_list(context.user_id())

        return json.dumps(response)