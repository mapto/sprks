
__author__ = 'Zhanelya'


from environment import render_public as render
import session

class home:
    """ Controllers commonly need a reference to the model (db) and also views
       These are declared in environment
    """

    def GET(self):
        session.mysession.session.loggedin = False
        session.mysession.session.user = 'Anonymous'
        session.mysession.session.date = ""
        return render.home()


