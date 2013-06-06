import web
import string
import json

render = web.template.render('templates/')

urls = (
    '/', 'index',
    '/add', 'add'
)

db = web.database(dbn='mysql', user='root', pw='1234', db='dbtest')

class index:

    def func(self, x):
        return x + 1

    def GET(self):
        id_tmp = 'test'
        result_get = db.select('pw_policy', where="id=$id_tmp", vars=locals())[0]

        return render.index(result_get.id, result_get.plen, result_get.psets,
                            result_get.pdict, result_get.phist, result_get.prenew,
                            result_get.pattempts, result_get.pautorecover)

class add:
    def POST(self):
        form = web.input()

        result = db.insert('pw_policy', id=form.id, plen=form.plen,
                           psets=form.pdict, pdict=form.pdict,
                           phist=form.phist, prenew=form.prenew,
                           pattempts=form.pattempts, pautorecover=form.pautorecover)

        return render.index(form.id, form.plen, form.psets, form.pdict, form.phist,
                            form.prenew, form.pattempts, form.pautorecover)
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()