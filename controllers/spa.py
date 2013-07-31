__author__ = 'Zhanelya'
import web
from localsys.environment import context
from localsys import storage
import datetime
from models.users import users_model


class spa:

    def GET(self):

        render_globals = {
            'user_id': context.user_id,
            'username': context.username
        }

        if web.input().get('action') == 'logout':
            users_model.session_login(0)

        return web.template.render('views/', globals=render_globals).index()
