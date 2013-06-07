__author__ = 'zcabh_000'

import web
import json

class index:
    def populate(self, db):
        '''
         presumes that database is already connected
        '''
#        use this if table needs to be created
#        db.query('CREATE TABLE pw_policy (id VARCHAR(20), plen INT, psets INT, pdict BOOL, psim VARCHAR(20), prenew VARCHAR(20), pattempts BOOL, precovery VARCHAR(20));')
        db.query("INSERT INTO pw_policy(`id`, `plen`, `psets`, `pdict`, `psim`, `prenew`, `pattempts`, `precovery`) VALUES ('test1', 8, 3, 0, 'simple', 'annual', 0, 'manned');")
        db.query("INSERT INTO pw_policy(`id`, `plen`, `psets`, `pdict`, `psim`, `prenew`, `pattempts`, `precovery`) VALUES ('test2', 8, 3, 0, 'simple', 'annual', 0, 'manned');")
        db.query("INSERT INTO pw_policy(`id`, `plen`, `psets`, `pdict`, `psim`, `prenew`, `pattempts`, `precovery`) VALUES ('test3', 8, 3, 0, 'simple', 'annual', 0, 'manned');")
        db.query("INSERT INTO pw_policy(`id`, `plen`, `psets`, `pdict`, `psim`, `prenew`, `pattempts`, `precovery`) VALUES ('test4', 5, 3, 0, 'simple', 'annual', 0, 'manned');")

    def GET(self):
        # make sure that the following line stays as per your local installation
        db = web.database(dbn='mysql', user='root', pw='1234', db='sprks')
#       when using sqlite instead of mysql
#        db = web.database(dbn='sqlite', db='sprks')

#        self.populate(db) # use this line if database needs to be created
        table = db.select('pw_policy')

        return "<h2>hello world</h2>" + json.dumps(table[0])
