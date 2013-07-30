__author__ = 'Zhanelya'
#copied from controllers.user with some minor changes

import json
import web

from localsys.environment import *

from localsys.storage import path
from models.users import users_model
from models.policies import policies_model
from libraries.utils import hash_utils
from models.oracle import prophet

render = web.template.render('views/', globals=render_globals)


class account:
    """
    Handles login, and REST API for login/registration.
    """

    def GET(self):
        """
        If action parameter is specified =='logout', logs out user. Else displays login screen
        """

        if web.input().get('action', '') == 'logout':
            users_model.session_login(0)

        raise web.seeother(path + '/')

    def POST(self):
        """
        Authenticates user
        """
        web.header('Content-Type', 'application/json')

        if context.user_id() > 0:
            users_model.session_login(context.user_id())
            return json.dumps(
                {
                    'success': True,
                    'messages': ['Successful login']
                }
            )
        else:
            return json.dumps(
                {
                    'success': False,
                    'messages': ['Invalid username/password']
                }
            )

    def PUT(self, a, username=''):
        """
        Stores user details into database.
        And, if needed, populates tables for first-time user
        """
        payload = json.loads(web.data())
        password = payload.get('password')
        email = payload.get('email')

        web.header('Content-Type', 'application/json')

        if password is None or email is None or username == '' or email == '':
            return json.dumps(
                {
                    'success': False,
                    'messages': ['Username/email/password cannot be empty']
                }
            )

        user_id = users_model().register(username, password, email)

        if user_id == 0:
            return json.dumps(
                {
                    'success': False,
                    'messages': ['User already exists']
                }
            )
        elif user_id > 0:
            if payload.get('autologin', False):
                users_model.session_login(user_id)
            web.ctx.status = '201 Created'
            policies_model.populate_policies(user_id, start_date)
            prophet().insert_score(user_id, 1, 1, start_date)
            prophet().insert_score(user_id, 2, 1, start_date)
            return json.dumps(
                {
                    'success': True,
                    'messages': ['User registered']
                }
            )
        else:
            return json.dumps(
                {
                    'success': False,
                    'messages': ['Database error']
                }
            )


class password:
    """
    Handles password management
    """

    def GET(self, a=0, token=0):
        """
        Handles password recovery from link sent by email
        First loads the page with (0,0),
        then handles the request and logs in user with ('/', token)

        for rendering page: a = 0, token = 0
        for sending message: a = '/', token = token written to DB for password recovery
        """

        web.header('Content-Type', 'application/json')

        if token == 0:                      #render page
            return render.skeleton_spa()
        else:                               #return message to ajax call for password recovery
            user_id = users_model.password_recovery_user(token)

            if user_id > 0:
                users_model.session_login(user_id)
                return json.dumps(
                    {
                        'success': True,
                        'user_id': user_id,
                        'messages': ['Please change your password']
                    }
                )
            else:
                return json.dumps(
                    {
                        'success': False,
                        'user_id': user_id,
                        'messages': ['User does not exist']
                    }
                )

    def PUT(self, a, arg1=0):
        """
        Changes password for specified user_id
        """

        user_id = int(arg1)
        print(user_id)
        payload = json.loads(web.data())
        user_model = users_model()

        web.header('Content-Type', 'application/json')

        if not (user_id > 0):
            return json.dumps(
                {
                    'success': False,
                    'messages': ['Invalid user_id specified']
                }
            )

        if user_id == context.user_id() or user_id == user_model.password_recovery_user(payload.get('token', '')):
            if user_model.update_password(user_id, payload['password']):
                if payload.get('autologin', False) and context.user_id() != user_id:
                    # Auto-login user whose password's changed.
                    users_model.session_login(user_id)
                return json.dumps(
                    {
                        'success': True,
                        'messages': ['Password changed']
                    }
                )
            return json.dumps(
                {
                    'success': False,
                    'messages': ['Database error']
                }
            )

        return json.dumps(
            {
                'success': False,
                'messages': ['Unauthorized request']
            }
        )

    def POST(self, a, arg1=0):
        """
        Creates password recovery request, taking argument as user_id (default) or username
        """
        try:
            uid_type = json.loads(web.data()).get('uid_type','')
        except ValueError:
            uid_type = ''

        token = hash_utils.random_hex()

        web.header('Content-Type', 'application/json')

        if uid_type == 'username':
            user_email = users_model().request_password(token, users_model.get_user_id(arg1))
        elif uid_type == 'user_id' or 'uid_type' == '':
            user_email = users_model().request_password(token, int(arg1))
        else:
            return json.dumps(
                {
                    'success': False,
                    'messages': ['Unknown uid type']
                }
            )

        if user_email == '':
            return json.dumps(
                {
                    'success': False,
                    'messages': ['User not found']
                }
            )

        try:
            web.config.smtp_server = 'smtp.gmail.com'
            web.config.smtp_port = 587
            web.config.smtp_username = 'sprkssuprt@gmail.com'
            web.config.smtp_password = 'sprks123456789'
            web.config.smtp_starttls = True
            web.sendmail('sprkssuprt@gmail.com', user_email, 'Password recovery',
                         'http://' + web.ctx.host + web.ctx.homepath + '/password_spa#token=' + token)
            return json.dumps(
                {
                    'success': True,
                    'messages': ['Password recovery email sent']
                }
            )
        except Exception:
            return json.dumps(
                {
                    'success': False,
                    'messages': ['Server error']
                }
            )
