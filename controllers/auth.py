import json

import web

import environment
from environment import render_public as render
from models.users import users_model


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
            return json.dumps({'errors': []})
        else:
            return json.dumps({'errors': ['Invalid username/password']})


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
            return json.dumps({'errors': ['User already exists']})
        elif user_id > 0:
            environment.session.user_id = user_id
            return json.dumps({'errors': []})
        else:
            return json.dumps({'errors': ['Database error']})