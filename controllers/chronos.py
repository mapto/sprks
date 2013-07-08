import json
import web
import localsys
from localsys.environment import context


class chronos:
    def POST(self):
        payload = json.loads(web.data())
        web.header('Content-Type', 'application/json')

        if context.user_id() == 0:
            return json.dumps({
                'success': False,
                'messages': ['Authorization failed.']
            })



        # if date is first day of month
            # payload.get('policyUpdate')

        # if event occured on the previous day
            # payload.get('intervention')



    def sync_history(self, date, new_costs):
        pass

    def prophesize(self):
        pass