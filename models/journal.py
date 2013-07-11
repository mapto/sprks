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

    @classmethod
    def last_sync(cls, user_id):
        """
        Given user_id, returns the date of the most recent sync.
        """
#        return date_utils.iso8601_to_date(db.query('SELECT date FROM policies ORDER BY date DESC LIMIT 1')[0].date)
        return db.query('SELECT date FROM policies ORDER BY date DESC LIMIT 1')[0].date

    @classmethod
    def first_due_event_day(cls, user_id, last_sync_date):
        """
        Returns the date for the first event due after previous sync. If no event found, returns none.
        """
        # TODO
        'SELECT date FROM journal WHERE user_id=user_id AND committed=false AND date<$last_sync_day ' \
        'GROUP BY date ORDER BY date DESC LIMIT 1'

    @classmethod
    def policy_review_due(cls, client_date, last_sync_date):
        """
        Returns true if a policy review was due since the last sync.
        """
        # TODO handle new year
        if (client_date.month - last_sync_date.month) > 0 or (client_date.year - last_sync_date.year) > 0:
            pass

    @classmethod
    def clear_history(cls, user_id, date):
        """
        Clears uncommitted entries in the journal for specified user_id on or after the specified date.
        """
        'DELETE FROM journal WHERE user_id=$user_id AND committed=false AND date>=$date'

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

            records.first_due_event_day(user_id, last_sync_date)
            # if any events were skipped, go to the day of the first missed event

            # if policy update is due, go to first day of new month

            records.policy_review_due(client_date, last_sync_date)

            return client_date
