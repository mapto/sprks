import json
import web
import session
from models.prophet import magic8


class chronos:

    def POST(self):
        request = json.loads(web.data())

        if session.mysession.session.loggedin:
            user_id = session.mysession.session.id

        else:
            raise web.seeother('/home')


    def commit_history(self, user_id, date, recent_costs):
        pass

    def prophesize(self):
        pass