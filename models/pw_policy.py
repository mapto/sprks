__author__ = 'Horace'

from settings import settings
from libraries import db_helper


class pw_policy_model:

    def update(self, where, values):
        """
        Executes UPDATE operation given where/dict and values/dict on pw_policy table.
        """
        return settings().db.query(db_helper.update_helper.stringify('pw_policy', where, values), vars=locals())