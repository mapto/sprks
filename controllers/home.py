
__author__ = 'Zhanelya'


from environment import render_public as render

class home:
    """ Controllers commonly need a reference to the model (db) and also views
       These are declared in environment
    """

    def GET(self):
        return render.home()


