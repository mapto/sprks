import json
import web
from localsys.environment import context
from libraries.utils import date_utils
from models.policies import policies_model
from models.journal import records
from models.oracle import prophet


class chronos:

    def POST(self):
        """
        Listens to POST requests for main Chronos API
        """

        payload = json.loads(web.data())
        web.header('Content-Type', 'application/json')

        policy_accept = False

        try:
            client_date = date_utils.iso8601_to_date(payload.get('date', '2014-01-06'))
        except ValueError:
            client_date = date_utils.iso8601_to_date('2014-01-06')

        policy_update = payload.get('policyUpdate')

        if context.user_id() == 0:
            return json.dumps({
                'success': False,
                'messages': ['Unauthorized']
            })

        journal = records(context.user_id())

        # corrected_sync_date backtracks if client submits invalid date.
        corrected_sync_date, event_accept = journal.validate_sync_date(client_date)
        #corrected_sync_date, event_accept = client_date, True

        if corrected_sync_date.day == 1:
            policy_accept = True
            if policy_update is None:
                # Expecting a policy update, but not found.
                #corrected_sync_date -= timedelta(days=1)
                # event_accept will always be false (backtracking one day before the next earliest sync point)
                event_accept = False
                # Expecting a policy update, but not found. Uses previous policy.
                policies_model.commit_same_policy(corrected_sync_date)
            else:
                policies_model.commit_policy_update(policy_update, corrected_sync_date)
                
        journal.commit_history(corrected_sync_date)

        if event_accept or policy_accept:
            journal.clear_prophecy(corrected_sync_date)
            prophecy = prophet.prophesize(context.user_id(), corrected_sync_date)
            print "prophecy " + prophecy
            journal.record_prophecy(prophecy)

        response = {
            'date': corrected_sync_date.isoformat(),
            'policyAccept': policy_accept,
            'eventAccept': event_accept,
            'calendar': journal.get_calendar(corrected_sync_date)
        }

        if payload.get('initPolicy', False):
            response['policy'] = policies_model.get_policies_list(context.user_id())

        return json.dumps(response)


class event_handler:
    def POST(self):
        payload = json.loads(web.data())
        client_date = date_utils.iso8601_to_date(payload.get('date', '2014-01-06'))
        if context.user_id() == 0:
            return json.dumps({
                'success': False,
                'messages': ['Unauthorized']
            })
        journal = records(context.user_id())
        journal.commit_history(client_date)
        return "OK"


class policy_update_handler:
    def POST(self):
        payload = json.loads(web.data())
        client_date = date_utils.iso8601_to_date(payload.get('date', '2014-01-06'))
        if context.user_id() == 0:
            return json.dumps({
                'success': False,
                'messages': ['Unauthorized']
            })
        policy_update = payload.get('policyUpdate')
        if client_date.day == 1:
            policies_model.commit_policy_update(policy_update, client_date)
        else:
            return json.dumps({
                'success': False,
                'messages': ['Commits are only allowed at the end of month']
            })
        journal = records(context.user_id())
        journal.clear_prophecy(client_date)
        prophecy = prophet.prophesize(context.user_id(), client_date)
        journal.record_prophecy(prophecy)
        response = {
            'date': client_date.isoformat(),
            'policyAccept': True,
            'eventAccept': False,
            'calendar': journal.get_calendar(client_date)
        }
        return json.dumps(response)


class resume_game:
    def POST(self):
        if context.user_id() == 0:
            return json.dumps({
                'success': False,
                'messages': ['Unauthorized']
            })
        journal = records(context.user_id())
        client_date = journal.get_last_sync()
        response = {
            'date': client_date.isoformat(),
            'policyAccept': False,
            'eventAccept': False,
            'calendar': journal.get_calendar(client_date),
            'policy': policies_model.get_policies_list(context.user_id())
        }
        return json.dumps(response)