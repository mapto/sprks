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
        db.query("INSERT INTO pw_policy VALUES ('test1', 6, 2, true, 'strict', 'never', true, 'auto')")
        finalresult="{\"prenew\": \"annual\", \"pattempts\": 0, \"pdict\": 0, \"psets\": 3, \"psim\": \"simple\", \"precovery\": \"manned\", \"plen\": 8, \"id\": \"test\"}"
        """

        results = db.query("SELECT * FROM pw_policy WHERE id LIKE 'test'")

        finalresult=json.dumps(results[0])


        id = 'test'
        plen = '8'
        psets = '3'
        pdict = '0'
        psim = 'simple'
        prenew = 'annual'
        pattempts = '0'
        precovery = 'manned'

        return render.index(id, plen, psets, pdict, psim, prenew, pattempts, precovery)

class add:
    def POST(self):
        form = web.input()

        """n = db.insert('pw_policy', title=form.title)
        raise web.seeother('/')"""

        id = form.__getattr__("id")
        plen = form.__getattr__("plen")
        psets = form.__getattr__("psets")
        pdict = form.__getattr__("pdict")
        psim = form.__getattr__("psim")
        prenew = form.__getattr__("prenew")
        pattempts = form.__getattr__("pattempts")
        precovery = form.__getattr__("precovery")

        """n = db.insert('pw_policy', title=form.item)
        raise web.seeother('/')


        db.query("INSERT INTO pw_policy VALUES (id,plen,psets,pdict,psim,prenew,pattemps,precovery)")
        """


        result='id='+id+' '+'plen='+plen+' '+'psets='+psets+' '+'pdic='+pdict+' etc.'
        return result






if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()