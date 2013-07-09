from localsys.environment import render
import web


class home:

    def GET(self):
        return render.home()


class favicon:

    def GET(self):
        web.header("Content-Type", 'images/x-icon')
        return open('favicon.ico').read()