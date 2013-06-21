from environment import render_public as render


class preview:

    def GET(self):
        return render.realtimesim()

