from localsys import storage
from datetime import date
from localsys.storage import db
from localsys.environment import context
from libraries.utils import date_utils


class records:

    def commit_history(self, date):
        user_id = context.user_id()
        result = db.update('journal', commited=1, where="date<$date&&user_id=$user_id", vars=locals())
        # TODO create empty entry in journal noting a sync was performed
        return result


    @classmethod
    def clear_history(cls, user_id, date):
        """
        Clears uncommitted entries in the journal for specified user_id on or after the specified date.
        """
        db.query('DELETE FROM journal WHERE user_id=$user_id AND committed=false AND date>=$date', vars(locals()))

    @classmethod
    def last_sync(cls, user_id):
        """
        Given user_id, returns the date of the most recent sync. If no previous
        """
        result = db.query('SELECT date FROM policies WHERE user_id=$user_id AND committed=true '
                          'ORDER BY date DESC LIMIT 1', vars=locals())
        if len(result) > 0:
            return date_utils.iso8601_to_date(result[0].date)
        return None

    @classmethod
    def next_due_event_day(cls, user_id):
        """
        Given user_id, returns the date for the first event due after previous sync. If no event found, returns none.
        """
        result = db.query('SELECT date FROM journal WHERE user_id=$user_id AND committed=false '
                 'GROUP BY date ORDER BY date ASC LIMIT 1', vars=locals())
        if len(result) > 0:
            return date_utils.iso8601_to_date(result[0].date)
        return None

    @classmethod
    def next_due_policy_day(cls, last_sync_date):
        """
        Returns next day that policy review is due since the last sync.
        """
        month = last_sync_date.month + 1
        if month > 12:
            return date(last_sync_date.year+1, month-12, 1)
        else:
            return date(last_sync_date.year, month, 1)


    @classmethod
    def update_journal(self, userid, risk):
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
                        db.insert('journal', user_id=userid, date=date, cost=cost, incident_id=inc_id, commited=0)
        return whole_calendar

    @classmethod
    def sync_history(self, user_id, client_date):
        """
        Synchronizes history where possible, and returns the date that the client should resume at.
        The date returned should also be corrected so it can be checked whether a policy or event-triggered
        recalculation should be performed.
        """
        last_sync_date = records.last_sync(user_id)
        if client_date <= last_sync_date:
            # Client behind the server
            return last_sync_date
        else:
            # The client is ahead of the server date.

            records.next_due_event_day(user_id)
            # if any events were skipped, go to the day of the first missed event

            # if policy update is due, go to first day of new month

            records.next_due_policy_day(last_sync_date)

            return client_date
