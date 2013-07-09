from localsys.environment import render
import web


class home:

    def GET(self):
        return render.home()