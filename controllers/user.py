import json

import web

from localsys.environment import *
from models.users import users_model
from libraries.utils import hash_utils


class login:
    """
    Handles login
    """

    def GET(self):
        """
        If action parameter is specified =='logout', logs out user. Else displays login screen
        """

        if context.user_id() == 0:
            return render.login()

        if web.input().get('action', '') == 'logout':
            users_model.session_login(0)

        raise web.seeother('/')

    def POST(self):
        """
        Authenticates user
        """
        web.header('Content-Type', 'application/json')

        user_id = context.user_id()

        if user_id > 0:
            users_model.session_login(user_id)
            return json.dumps({
                'success': True,
                'msgs': ['Successful login']
            })
        else:
            return json.dumps({
                'success': False,
                'msgs': ['Invalid username/password']
            })


class register:
    """
    Handles user registration
    """
    def GET(self):
        if context.user_id() > 0:
            raise web.seeother('/')
        return render.register()

    def POST(self):
        """
        Stores user details into database.
        """
        payload = json.loads(web.data())
        user_id = users_model().register(payload['username'], payload['password'], payload['email'])

        web.header('Content-Type', 'application/json')
        if user_id == 0:
            return json.dumps({
                'success': False,
                'msgs': ['User already exists']
            })
        elif user_id > 0:
            users_model.session_login(user_id)
            web.ctx.status = '201 Created'
            return json.dumps({
                'success': True,
                'msgs': ['User registered'],
                'user_id': user_id
            })
        else:
            return json.dumps({
                'success': False,
                'msgs': ['Database error']
            })


class password:
    """
    Handles password management
    """

    def GET(self):

        user_id = context.user_id()
        if user_id > 0:
            return render.password_change(user_id, '')

        token = web.input().get('token','')
        user_id = users_model().password_recovery_user(token)
        if user_id == 0:
            return render.password_recover()
        else:
            return render.password_change(user_id, token)

    def PUT(self, a, arg1=0):
        """
        Changes password for specified user
        """

        user_id = int(arg1)
        payload = json.loads(web.data())
        user_model = users_model()

        web.header('Content-Type', 'application/json')

        if not (user_id > 0):
            return json.dumps({
                'success': False,
                'msgs': ['Invalid user_id specified']
            })

        if user_id == context.user_id() or user_id == user_model.password_recovery_user(payload.get('token', '')):
            if user_model.update_password(user_id, payload['password']):
                users_model.session_login(user_id)
                return json.dumps({
                    'success': True,
                    'msgs': ['Password changed']
                })
            return json.dumps({
                'success': False,
                'msgs': ['Database error']
                })

        return json.dumps({
            'success': False,
            'msgs': ['Unauthorized request']
        })

    def POST(self, a, arg1=0):
        """
        Creates password recovery request, taking argument as user_id (default) or username
        """
        payload = json.loads(web.data())
        token = hash_utils.random_hex()

        web.header('Content-Type', 'application/json')
        uid_type = payload.get('uid_type','')
        if uid_type == 'username':
            user_email = users_model().request_password(token, users_model.get_user_id(arg1))
        elif uid_type == 'user_id' or 'uid_type' == '':
            user_email = users_model().request_password(token, int(arg1))
        else:
            return json.dumps({
                'success': False,
                'msgs': ['Unknown uid type']
            })

        if user_email == '':
            return json.dumps({
                'success': False,
                'msgs': ['User not found']
            })

        try:
            web.config.smtp_server = 'smtp.gmail.com'
            web.config.smtp_port = 587
            web.config.smtp_username = 'sprkssuprt@gmail.com'
            web.config.smtp_password = 'sprks123456789'
            web.config.smtp_starttls = True
            web.sendmail('sprkssuprt@gmail.com', user_email, 'Password recovery',
                         'http://' + web.ctx.host + web.ctx.homepath + '/password?token=' + token)
            return json.dumps({
                'success': True,
                'msgs': ['Password recovery email sent']
            })
        except Exception:
            return json.dumps({
                'success': False,
                'msgs': ['Server error']
            })