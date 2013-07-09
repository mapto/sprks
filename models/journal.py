__author__ = 'admin'

from localsys import storage
from controllers.chronos import chronos
from datetime import datetime


class records:
    default_calendar = {'date': '2014/1/14',
                        'calendar': [
    {
      'date': '2014/1/20',
      'events': [
        {
        'incdt_id': 5,
        'cost': 2000
        }
      ]
    },
    {
      'date': '2014/1/21',
      'events': []
    },
    {
      'date': '2014/2/5',
       'events': [
        {
          'incdt_id': 1,
          'cost': 7000000
        },
        {
          'incdt_id': 4,
          'cost': 5000
        }
      ]
    },
    {
      'date': '2014/2/7',
      'events': [
        {
          'incdt_id': 8,
          'cost': 1000
        }
      ]
    }
  ] ,
                        'policyAccept':'true',
                        'interventionAccept': 'true'}

    def commit_history(self, date):
        result = storage.db.update('journal', commited=1, where="date<$date&&user_id=$context.user_id()", vars=locals())
        return result

    def record_prophecy(self):
        pass

    def validate_journal(self, cost, date, user_id):
        sum = storage.db.select('journal', what="SUM(cost) as sum", where="date<$date and user_id=$user_id and commited!=1", vars=locals())[0].sum
        self.commit_history(date)
        if sum == cost:
            return 1
        else:
            return 0

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
                    dtt = datetime.strptime(date, "%Y/%m/%d")
                else:
                    for event in dates[key]:
                        inc_id = event['incdt_id']
                        cost = event['cost']
                        storage.db.insert('journal', user_id=userid, date=dtt.strftime("%Y/%m/%d"), cost=cost, incident_id=inc_id, commited=0)
        return whole_calendar