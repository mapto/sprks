import json
import web
import localsys
from localsys.environment import context


class chronos:
    def POST(self):
        request = json.loads(web.data())

        if context.user_id() > 0:
            user_id = context.user_id()

        else:
            raise web.seeother('/home')


    def commit_history(self, user_id, date, recent_costs):
        pass

    def prophesize(self):
        pass