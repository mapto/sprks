__author__ = 'Horace'

from environment import db


class policies_model:

    def get_policy_history(self, id):
        history = db.query('SELECT * FROM pw_policy JOIN users ON userid = Id WHERE username = "' + id + '" ORDER BY date LIMIT 1')
#        history = db.select('pw_policy', where="userid=$id", order="date", vars=locals())
        return history[0]



