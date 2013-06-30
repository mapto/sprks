import json

import web

import environment
from environment import render_public as render
from models.users import users_model
from libraries.utils import hash_utils
from libraries.user_helper import auth


class login:
    """
    Handles login
    """

    def GET(self):
        environment.session.user_id = 0
        return render.login()

    def POST(self):
        """
        Authenticates user
        """
        payload = json.loads(web.data())
        user_id = users_model().authenticate(payload['username'], payload['password'])

        web.header('Content-Type', 'application/json')
        if user_id > 0:
            environment.session.user_id = user_id
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
        if environment.session.user_id > 0:
            raise web.seeother('/pwpolicy')
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
            environment.session.user_id = user_id
            web.ctx.status = '201 Created'
            return json.dumps({
                'success': True,
                'msgs': ['User registered']
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

        user_id = auth().user_id()
        if user_id > 0:
            return environment.render_private.password_change(user_id, '', users_model().get_username(environment.session.user_id))

        token = getattr(web.input(), 'token', '')
        user_id = users_model().password_recovery_user(token)
        if user_id == 0:
            return render.password_recover()
        else:
            return render.password_change(user_id, token)

    def PUT(self):
        """
        If user is logged in XOR valid password recovery token is included, changes user password.
        """

        payload = json.loads(web.data())
        user_model = users_model()

        current_user_id = auth().user_id()

        token_user_id = 0
        if 'token' in payload:
            token = payload['token']
            token_user_id = user_model.password_recovery_user(token)

        if token_user_id == 0:
            if current_user_id == 0:
                return json.dumps({
                    'success': False,
                    'msgs': ['Invalid token and user not logged in']
                })
            else:
                user_id = current_user_id
        else:
            if current_user_id == 0:
                user_id = token_user_id
                user_model.update_recovery_status(token)
            else:
                return json.dumps({
                    'success': False,
                    'msgs': ['Current user and password recovery token do not match']
                })

        if user_model.update_password(user_id, payload['password']):
            environment.session.user_id = user_id
            web.ctx.status = '200 OK'
            return json.dumps({
                'success': True,
                'msgs': ['Successfully changed password']
            })
        else:
            return json.dumps({
                'success': False,
                'msgs': ['Database error - password not updated']
                })

    def POST(self):
        """
        Sends password recovery email to user.
        """
        payload = json.loads(web.data())
        username = payload['username']
        token = hash_utils.random_hex(username)
        user_email = users_model().request_password(username, token)
        web.header('Content-Type', 'application/json')
        if user_email == '':
            return json.dumps({
                'success': False,
                'msgs': ['User not found']
            })
        else:
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
