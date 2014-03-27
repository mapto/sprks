import json
import web
from localsys.environment import context
from libraries.utils import date_utils
from models.policies import policies_model
from models.journal import records
from models.oracle import prophet


class event_handler:
    def POST(self):
        web.header('Content-Type', 'application/json')

        payload = json.loads(web.data())
        client_date = date_utils.iso8601_to_date(payload.get('date', '2014-01-06'))
        if context.user_id() == 0:
            return json.dumps({
                'success': False,
                'messages': ['Unauthorized']
            })
        journal = records(context.user_id())
        journal.commit_history(client_date)
        return json.dumps({
            'success': True,
            'messages': ['Event committed']
        })


class policy_update_handler:
    def POST(self):
        """
        Handles policy updates and returns calendar.

        :return: JSON dump
        """
        web.header('Content-Type', 'application/json')

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
        journal.clear_prophecy(client_date, policy_update)
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
    def GET(self):
        web.header('Content-Type', 'application/json')

        if context.user_id() == 0:
            return json.dumps({
                'success': False,
                'messages': ['Unauthorized']
            })
        journal = records(context.user_id())
        client_date = journal.get_last_sync()

        start_date = date_utils.iso8601_to_date('2014-01-06')
        days_delta = (client_date - start_date).days
        if days_delta >= 176:         #6 months have passed (July, 1)
            employees_number = 9
        elif days_delta >= 85:        #3 months have passed (April, 1)
            employees_number = 3
        else:
            employees_number = 1

        response = {
            'date': client_date.isoformat(),
            'policyAccept': False,
            'eventAccept': False,
            'calendar': journal.get_calendar(client_date),
            'policy': policies_model.get_policies_list(context.user_id()),
            'employees_number': employees_number
        }

        return json.dumps(response)

class recent_events:
    def GET(self):
        journal = records(context.user_id())
        result = journal.get_recent_events()

        #return at most 31 latest happened events from the journal table
        return json.dumps(result)