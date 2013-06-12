__author__ = 'zhanelya'

import web
from settings import settings

class score:
    def GET(self):
        render = settings().render
        return render.score(8,2,3)