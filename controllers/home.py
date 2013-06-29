
__author__ = 'Zhanelya'


from environment import render_public as render
import environment


class home:
    """ Controllers commonly need a reference to the model (db) and also views
       These are declared in environment
    """

    def GET(self):
        environment.session.user_id = 0
        return render.home()


