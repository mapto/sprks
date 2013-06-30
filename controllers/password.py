import json

import web

from libraries.utils import hash_utils
from models.users import users_model
import environment
from environment import render_public as render
from libraries.user_helper import auth


class manage:
    """
    Handles password management
    """

    def GET(self):

        user_id = auth().user_id()
        if user_id > 0:
            return environment.render_private.password_change(user_id, '')

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
                return json.dumps({'errors': ['Invalid token and user not logged in']})
            else:
                user_id = current_user_id
        else:
            if current_user_id == 0:
                user_id = token_user_id
                user_model.update_recovery_status(token)
            else:
                return json.dumps({'errors': ['Current user and password recovery token do not match']})

        if user_model.update_password(user_id, payload['password']):
            environment.session.user_id = user_id
            return json.dumps({'errors': []})
        else:
            return json.dumps({'errors': ['Database error - password not updated']})

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
            return json.dumps({'errors': ['User not found']})
        else:
            web.config.smtp_server = 'smtp.gmail.com'
            web.config.smtp_port = 587
            web.config.smtp_username = 'sprkssuprt@gmail.com'
            web.config.smtp_password = 'sprks123456789'
            web.config.smtp_starttls = True
            web.sendmail('sprkssuprt@gmail.com', user_email, 'Password recovery',
                         'http://localhost:8080/password?token=' + token)
            return json.dumps({'errors': []})
