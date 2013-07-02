__author__ = 'admin'

from localsys import storage
from controllers.chronos import chronos

class records:
    def commit_history(self, date):
        result = storage.db.update('journal', commited=1, where="date<$date", vars=locals())
        return result

    def record_prophecy(self):
        pass

    def validateJournal(self, cost, date, user_id):
        sum = storage.db.sum('journal', where="date<$date and user_id=$user_id", vars=locals())
        self.commit_history(date)
        if sum == cost:
            return 1
        else:
            return 0

    def updateJournal(self, risk, userid):
        calendar = chronos.prophesize(risk)["prophecy"]
        for dates in calendar:
            for key in dates:
                date = ""
                cost = ""
                inc_id = ""
                if key == 'date':
                    date = dates[key]
                else:
                    for event in dates[key]:
                        inc_id = event['incident_id']
                        cost = event['cost']
                storage.db.insert('journal', user_id=userid, date=date, cost=cost, incident_id=inc_id, commited=0)
        return calendar