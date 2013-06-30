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

        token = web.input().token
        user_id = users_model().password_recovery_status(token)
        if user_id == 0:
            return render.password_recover()
        else:
            return render.password_change(user_id, token)

    def PUT(self):
        """
        If user is logged in XOR valid password recovery token is included, changes user password.
        """

        payload = json.loads(web.data())

        current_user_id = auth().user_id()
        if 'token' in payload:
            token = payload['token']
            user_id = users_model().password_recovery_valid(token)
            if user_id == 0 and current_user_id == 0:
                return json.dumps({'errors': ['Invalid token and user not logged in']})
        # TODO LOGIC ERROR
        if users_model().update_password(user_id, payload['password']):
            users_model().update_recovery_status(token)
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
