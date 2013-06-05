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
        """pw_Policy=db.select('pw_policy')
        proper DB search needs to be implemented
        """
        results = db.query("SELECT * FROM pw_policy WHERE id LIKE 'test'")
        finalresult=json.dumps(results[0])
        """json translation to vars is needed"""

        id = 'test'
        plen = '8'
        psets = '3'
        pdict = '0'
        phist = '1'
        prenew = '1'
        pattempts = '0'
        pautorecover = '1'

        return render.index(id, plen, psets, pdict, phist, prenew, pattempts, pautorecover)

class add:
    def POST(self):
        form = web.input()

        result = db.insert('pw_policy', id = form.id, plen = form.plen,
                           psets = form.pdict, pdict = form.pdict,
                           phist = form.phist, prenew = form.prenew,
                           pattempts = form.pattempts, pautorecover = form.pautorecover)

        return render.index(form.id, form.plen, form.psets, form.pdict, form.phist,
                            form.prenew, form.pattempts, form.pautorecover)
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()