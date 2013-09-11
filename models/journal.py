from datetime import date
from localsys.storage import db
from datetime import timedelta
import datetime


class records:

    def __init__(self, user_id):
        self.user_id = user_id

    def commit_history(self, date):
        """
        Sets all events before the specified date to be committed.
        """
        result = db.update('journal', committed=1, where="date<=$date&&user_id=$self.user_id", vars=locals())
        return result

    def clear_prophecy(self, date):
        """
        Clears uncommitted entries in the journal for specified user_id on or after the specified date. Returns None.
        """
        db.query('DELETE FROM journal WHERE user_id=$self.user_id AND committed=false AND date>=$date', vars=locals())

    def __last_sync(self):
        """
        Given user_id, returns the date of the most recent sync.
        """

        last_policy_sync = db.query('SELECT date FROM policies WHERE user_id=$self.user_id '
                                    'ORDER BY date DESC LIMIT 1', vars=locals())

        last_event_sync = db.query('SELECT date FROM journal WHERE user_id=$self.user_id AND committed=1 '
                                   'ORDER BY date DESC LIMIT 1', vars=locals())

        # Query responses are iterators. As a result every time last_policy_sync[0] is called, it pops that item.
        # Next time last_policy_sync[0] is called, the response is different. Using local variables to work around this.
        policy_date = last_policy_sync[0].date


        #CANT COMPARE DATETIME AND DATE!!!
        if len(last_event_sync) > 0:
            event_date = last_event_sync[0].date
            if event_date > policy_date:
                return event_date

        return policy_date

    def get_last_sync(self):
        return self.__last_sync()

    def __next_sync(self, last_sync_date):
        """
        For the given user and a last sync date, returns the next sync due (whether it be policy sync or event sync).
        :param last_sync_date:
        """

        next_due_policy_date = self.__next_due_policy_date(last_sync_date)

        next_due_event_date = self.__next_due_event_date()

        """
        Cant compare datetime.datetime and datetime.date!!!
        """
        if next_due_event_date is not None and next_due_event_date <= next_due_policy_date:
            return next_due_event_date, True

        return next_due_policy_date, False

    def __next_due_event_date(self):
        """
        Given user_id, returns the date for the first event due after previous sync. If no event found, returns none.
        """

        result = db.query('SELECT date FROM journal WHERE user_id=$self.user_id AND committed=false '
                          'GROUP BY date ORDER BY date ASC LIMIT 1', vars=locals())
        if len(result) > 0:
            return result[0].date
        return None

    def __next_due_policy_date(self, last_sync_date):
        """
        Returns next day that policy review is due since the last sync.
        """

        month = last_sync_date.month + 1

        if month > 12:
            return date(last_sync_date.year+1, month-12, 1)

        return date(last_sync_date.year, month, 1)

    def record_prophecy(self, prophecy):
        """
        For given user_id and prophecy (proprietary format), decodes the prophecy and stores them in the journal.
        Accepts a prophecy in the following form:
        [
            {
                'date': 'YYYY-MM-DD'
                'incident_id': 1,
                'cost': 5000000
            },
            ...
        ]
        """
        #for event in prophecy.iteritems():
        for event in prophecy:
            event['user_id'] = self.user_id
            event['committed'] = 0

        db.multiple_insert('journal', values=prophecy)

    def get_calendar(self, sync_date):
        """
        Retrieve all events (past or future) for given user_id for month that the specified date falls on.
        Returns a custom dictionary-based data structure based on the REST API JSON spec.
        :param sync_date:
        """

        start_date = datetime.date(sync_date.year, sync_date.month, 1)

        end_date = (start_date + timedelta(days=32)).replace(day=1)

        raw_calendar = db.query('SELECT * FROM journal '
                                'WHERE user_id=$self.user_id AND date>=$start_date AND date<$end_date', vars=locals())

        calendar = {}
        # Converts database results into dictionary
        for event in raw_calendar:
            if event.date not in calendar:
                calendar[event.date] = {
                    'date': event.date.isoformat(),
                    'events': []
                }
            calendar[event.date]['events'].append({
                'incdt_id': event.incident_id,
                'cost': event.cost,
                'employee': event.employee,
                'location': event.location,
                'device': event.device
            })

        calendar_array = []
        # Converts calendar dictionary into array
        for date, agenda in sorted(calendar.iteritems()):
            calendar_array.append(agenda)
        print "calendar"
        print calendar_array
        return calendar_array

    def validate_sync_date(self, client_date):
        """
        Returns the date that the client should resume at.
        The date returned should be corrected so it can be checked whether a policy or event-triggered
        recalculation should be performed.
        """
        last_sync_date = self.__last_sync()

        print 'last sync date' + last_sync_date.isoformat()
        print 'client date' + client_date.isoformat()
        if client_date <= last_sync_date:
            # Client behind the last sync date.
            print 'client date <= last sync date'
            return last_sync_date, False


        next_sync_date, event_accept = self.__next_sync(last_sync_date)

        print 'next sync date' + next_sync_date.isoformat()

        if client_date >= next_sync_date:
            # Client is ahead of the next predicted sync date.
            corrected_sync_date = next_sync_date
        else:
            # Client is at an arbitrary date between next_sync_date and last_sync_date for some weird reason.
            corrected_sync_date = client_date

        return corrected_sync_date, event_accept

    def get_recent_events(self):
        return self.__recent_events()

    def __recent_events(self):
        """
        Returns the latest events for current user, ordering them by date and choosing the committed events only.
        """

        events_list = []
        #restrict to events which have already happened
        restrict_committed = 'AND journal.committed=1 '
        #restrict to the latest events
        #assuming that max 1 event/day can happen and there are max 31 days in 1 month
        restrict_latest = 'LIMIT 31'

        result = db.query(
            'SELECT * FROM journal '
            'WHERE journal.user_id=$self.user_id ' + restrict_committed +
            'ORDER BY journal.date DESC ' + restrict_latest, vars=locals())

        for row in result:
            tmp = {}
            for key, value in row.iteritems():
                tmp[key] = str(value)
            events_list.append(tmp)
        return events_list

