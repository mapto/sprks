__author__ = 'zcabh_000'
import web
import json

class index:
    def func(self, x):
        return x + 1

    def GET(self):
        db = web.database(dbn='mysql', user='root', pw='12345', db='sprks')
        table = db.select('pw_policy')
        return json.dumps(table[0]) + " hello world2"
        #return "test"