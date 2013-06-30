__author__ = "Dan"

import web
import json
import environment
from environment import render_public as render
from models.users import users_model


class register:
    def GET(self):
        if environment.session.user_id > 0:
            raise web.seeother('/pwpolicy')
        return render.register()

    def POST(self):
        """
        Stores user details into 'users' table.
        """
        payload = json.loads(web.data())
        user_id = users_model().register(payload['username'], payload['password'], payload['email'])

        web.header('Content-Type', 'application/json')
        if user_id == 0:
            return json.dumps({
                'errors': ['User already exists']});
        elif user_id > 0:
            environment.session.user_id = user_id
            return json.dumps({
                'errors': []});
        else:
            return json.dumps({
                'errors': ['Database error']});