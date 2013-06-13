__author__ = "Dan"

import web
import session
from environment import render_public as render
from models.users import users_model


class register:
    def GET(self):
        return render.register()

    def POST(self):
        """
        Stores user details into 'users' table.
        """
        post_data = web.input()
        reg_id = users_model.register(post_data.username, post_data.password, post_data.email)

        if reg_id == 0:
            return render.register("User already exists")
        elif reg_id > 0:
            session.mysession.session.loggedin=True
            session.mysession.session.user=post_data.username
            session.mysession.session.id=reg_id
            raise web.seeother('/pwpolicy')
        else:
            return render.register("Database error")