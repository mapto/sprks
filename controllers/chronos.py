import json
import web
import localsys
from datetime import date
from localsys.environment import context


class chronos:
    def POST(self):
        payload = json.loads(web.data())
        web.header('Content-Type', 'application/json')

        if context.user_id() == 0:
            return json.dumps({
                'success': False,
                'messages': ['Unauthorized']
            })

        self.sync_history(payload.get('date'), payload.get('newCosts'))

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
            return json.dumps({
                'date': date(2000, 1, 1).isoformat(),
                'policyAccept': True,
                'interventionAccept': True,
                'calendar': [
                    {
                        # calendar
                    }
                ]
            })

    def sync_history(self, date, new_costs):
        pass

    def prophesize(self):
        """
        Generates calendar of future events.
        """
        pass