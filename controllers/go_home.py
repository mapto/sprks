__author__ = 'mapto'

import web

class go_home:
    """ Redirect to project home
    """

    def GET(self):
        raise web.seeother('/home')


