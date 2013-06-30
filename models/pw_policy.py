__author__ = 'Horace'

from libraries import db_helper
from environment import db


class pw_policy_model:
    def update(self, where, values):
        """
        Generates query string using db_helper.update_helper.stringify, and runs db.query.
        """
        return db.query(db_helper.update_helper.stringify('pw_policy', where, values), vars=locals())

    def latest_policy(self):
        pass