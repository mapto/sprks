__author__ = 'zhanelya'

import web
from environment import render_private as render

class score:
    def GET(self):
        return render.score(8,2,3)