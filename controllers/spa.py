__author__ = 'Zhanelya'
import web
from localsys.environment import get_start_time
from localsys.environment import context
from localsys import storage
import datetime

render_globals = {
    'datetime': datetime,
    'get_start_time': get_start_time,
    'user_id': context.user_id,
    'username': context.username,
    'path': storage.path,
}
render = web.template.render('views/', globals=render_globals)


class spa:
    def GET(self):
        return render.skeleton_spa()
