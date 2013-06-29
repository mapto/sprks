__author__ = "Dan"

import web
import environment
from environment import render_public as render
from models.users import users_model


class register:
    def GET(self):
        # TODO shouldn't be able to register if already logged in
        return render.register()

    def POST(self):
        """
        Stores user details into 'users' table.
        """
        post_data = web.input()
        user_id = users_model().register(post_data.username, post_data.password, post_data.email)

        if user_id == 0:
            return render.register("User already exists")
        elif user_id > 0:
            environment.mysession.session.user_id = user_id
            raise web.seeother('/intro')
        else:
            return render.register("Database error")