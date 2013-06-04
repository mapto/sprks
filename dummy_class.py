import web
import json
import login
import dummy_index

urls = (
    '/', dummy_index.index,
         '/login', login.login
)





if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()