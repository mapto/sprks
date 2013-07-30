__author__ = 'Zhanelya'
import web
from localsys.environment import context
from localsys import storage
import datetime
from models.users import users_model

render_globals = {
    'datetime': datetime,
    'user_id': context.user_id,
    'username': context.username,
    'path': storage.path,
}
render = web.template.render('views/', globals=render_globals)


class spa:
    def GET(self):

        get_data = web.input()

        if get_data.get('action') == 'logout':
            users_model.session_login(0)

        return render.skeleton_spa()
