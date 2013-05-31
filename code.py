import web
import json

urls = (
    '/', 'index'
)


class index:

    def func(x):
        return x + 1

    def GET(self):
        db = web.database(dbn='mysql', user='user', pw='password', db='test')
        table = db.select('pw_policy')
        return json.dumps(table[0]) + " hello world2"

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()