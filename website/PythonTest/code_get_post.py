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
        phist = '2'
        prenew = '1'
        pattempts = '0'
        pautorecover = '1'

        return render.index(id, plen, psets, pdict, phist, prenew, pattempts, pautorecover)

class add:
    def POST(self):
        form = web.input()

        id = form.__getattr__("id")
        plen = form.__getattr__("plen")
        psets = form.__getattr__("psets")
        pdict = form.__getattr__("pdict")
        psim = form.__getattr__("phist")
        prenew = form.__getattr__("prenew")
        pattempts = form.__getattr__("pattempts")
        precovery = form.__getattr__("pautorecover")

        """n = db.insert('pw_policy', title=form.item)
        raise web.seeother('/')
        INSERT to DB needs to be implemented
        """


        result='id='+id+' '+'plen='+plen+' '+'psets='+psets+' '+'pdict='+pdict+' etc.'
        return result






if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()