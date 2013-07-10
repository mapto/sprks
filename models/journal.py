__author__ = 'admin'

from localsys import storage
from controllers.chronos import chronos
from datetime import datetime
from localsys.environment import context


class records:

    def commit_history(self, date):
        user_id = context.user_id()
        result = storage.db.update('journal', commited=1, where="date<$date&&user_id=$user_id", vars=locals())
        return result

    def record_prophecy(self):
        pass

    def validate_journal(self, user_id, date, new_costs):
        sum = storage.db.select('journal', what="SUM(cost) as sum", where="date<$date and user_id=$user_id and commited!=1", vars=locals())[0].sum
        self.commit_history(date)
        return sum == new_costs

    def update_journal(self, risk, userid):
        #calendar = chronos.prophesize(risk)["prophecy"]
        calendar = self.default_calendar["calendar"]
        whole_calendar = self.default_calendar
        for dates in calendar:
            for key in dates:
                date = ""
                cost = ""
                inc_id = ""
                if key == 'date':
                    date = dates[key]
                    dtt = date
                else:
                    for event in dates[key]:
                        inc_id = event['incdt_id']
                        cost = event['cost']
                        storage.db.insert('journal', user_id=userid, date=date, cost=cost, incident_id=inc_id, commited=0)
        return whole_calendar