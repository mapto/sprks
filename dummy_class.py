import web
import login
import register
import dummy_index

urls = (
    '/', dummy_index.index,
         '/login', login.login,
        '/register', register.register
)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()