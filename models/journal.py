__author__ = 'admin'

from localsys import storage
from datetime import datetime
from localsys.storage import db
from localsys.environment import context
from libraries.utils import date_utils


class records:

    def commit_history(self, date):
        user_id = context.user_id()
        result = db.update('journal', commited=1, where="date<$date&&user_id=$user_id", vars=locals())
        return result

    def record_prophecy(self):
        pass

    def validate_journal(self, user_id, date, new_costs):
        sum = db.select('journal', what="SUM(cost) as sum",
                                where="date<$date AND user_id=$user_id AND commited=false", vars=locals())[0].sum
        self.commit_history(date)
        return sum == new_costs

    @classmethod
    def last_sync(cls, user_id):
        """
        Given user_id, returns the date of the most recent sync.
        """
        return date_utils.iso8601_to_date(db.query('SELECT date FROM policies ORDER BY date DESC LIMIT 1')[0].date)

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