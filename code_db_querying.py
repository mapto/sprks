import web
import string
import json 

urls = (
    '/', 'index',
    '/add', 'add'
)

db = web.database(dbn='mysql', user='root', pw='1234', db='dbtest')

class index:
    def GET(self):
        pw_Policy=db.select('pw_policy')
        results = db.query("SELECT * FROM pw_policy WHERE id LIKE 'test'")
        finalresult=json.dumps(results[0])
      
       
        db.query("INSERT INTO pw_policy VALUES ('test1', 6, 2, true, 'strict', 'never', true, 'auto')")
        return finalresult


class add:
    def POST(self):
        i = web.input()
        n = db.insert('pw_policy', title=i.title)
        raise web.seeother('/')


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()