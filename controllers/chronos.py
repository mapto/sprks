import json
import web
import localsys


class chronos:
    def POST(self):
        request = json.loads(web.data())

        if localsys.session.user_id > 0:
            user_id = localsys.session.user_id

        else:
            raise web.seeother('/home')


    def commit_history(self, user_id, date, recent_costs):
        pass

    def prophesize(self):
        pass