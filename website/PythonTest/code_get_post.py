import web
import string
import json

render = web.template.render('views/')

urls = (
    '/', 'index',
    '/add', 'add'
)

class index:
    def populate(self, db):
        '''
         presumes that database is already connected
        '''
#       use this if table needs to be created
        db.query('CREATE TABLE pw_policy(id INT NOT NULL PRIMARY KEY, plen INT, psets INT, pdict BOOL, phist INT, prenew INT, pattempts BOOL, pautorecover BOOL);')

#       use this if table needs to be filled with values
        db.query("INSERT INTO pw_policy VALUES (1, 8, 3, 0, 1, 1, 0, 1);")
        db.query("INSERT INTO pw_policy VALUES (2, 8, 3, 0, 1, 1, 0, 1);")
        db.query("INSERT INTO pw_policy VALUES (3, 8, 3, 0, 1, 1, 0, 1);")
        db.query("INSERT INTO pw_policy VALUES (4, 5, 3, 0, 1, 1, 0, 1);")

    def func(self, x):
        return x + 1

    def GET(self):
        # make sure that the following line stays as per your local installation
        db = web.database(dbn='mysql', user='root', pw='1234', db='sprks')
#       when using sqlite instead of mysql
#       db = web.database(dbn='sqlite', db='sprks')

#        self.populate(db) # use this line if database table needs to be created and populated

        #use this variable to request any ID number
        id_tmp = 1
        check = db.select('pw_policy', where="id=$id_tmp", vars=locals())

        if check:
            notfound=0
            result_get = db.select('pw_policy', where="id=$id_tmp", vars=locals())[0]
            return render.index(result_get.id, result_get.plen, result_get.psets,
                            result_get.pdict, result_get.phist, result_get.prenew,
                            result_get.pattempts, result_get.pautorecover, notfound)
        else:
            notfound=1
            result_get = db.select('pw_policy', where="id=1", vars=locals())[0]
            return render.index(result_get.id, result_get.plen, result_get.psets,
                            result_get.pdict, result_get.phist, result_get.prenew,
                            result_get.pattempts, result_get.pautorecover, notfound)


class add:
    def POST(self):
        # make sure that the following line stays as per your local installation
        db = web.database(dbn='mysql', user='root', pw='1234', db='sprks')
#       when using sqlite instead of mysql
#       db = web.database(dbn='sqlite', db='sprks')

        form = web.input()
        id_tmp = form.id
        check = db.select('pw_policy', where="id=$id_tmp", vars=locals())
        if check:
            result = db.update('pw_policy', where='id = $form.id', plen=form.plen, psets=form.psets,
                                   pdict=form.pdict, phist=form.phist, prenew=form.prenew,
                                   pattempts=form.pattempts, pautorecover=form.pautorecover, vars=locals())
            print 'found id'+id_tmp
        else:
            result = db.insert('pw_policy', id=form.id, plen=form.plen,
                                   psets=form.psets, pdict=form.pdict,
                                   phist=form.phist, prenew=form.prenew,
                                   pattempts=form.pattempts, pautorecover=form.pautorecover)
            print 'id'+id_tmp+' does not exist'

        notfound=0
        return render.index(form.id, form.plen, form.psets, form.pdict, form.phist,
                            form.prenew, form.pattempts, form.pautorecover, notfound)
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()