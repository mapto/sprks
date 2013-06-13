import web
import session
import settings
from models.users import users_model


class register:
    profile = settings()
    render = profile.render

    def GET(self):
        return self.render.register()

    def POST(self):
        """
        Stores user details into 'users' table.
        """
        post_data = web.input()
        reg_id = users_model.register(post_data.username, post_data.password, post_data.email)

        if reg_id == 0:
            return self.render.register("User already exists")
        elif reg_id > 0:
            session.mysession.session.loggedin=True
            session.mysession.session.user=post_data.username
            session.mysession.session.id=reg_id
            raise web.seeother('/pwpolicy')
        else:
            return self.render.register("Database error")