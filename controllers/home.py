from localsys.environment import render


class home:

    def GET(self):
        return render.home()
