__author__ = 'Dan'

import web
from environment import render_public as render
from models.users import users_model


class pwrecovery:

    def GET(self, rand):
        username = users_model().pwrecovery_status(rand)
        if username == '':
            return "Invalid password recovery request"
        else:
            return render.pwrecovery(username)

    def POST(self):
        if web.ctx.env.get('HTTP_REFERER', '').find(web.ctx.host + '/pwrecovery') != -1:
            # greps [host]/pwrecovery within referer URI
            post_data = web.input()
            username = web.websafe(post_data.user)
            if users_model().update_password(username, web.websafe(post_data.Password)):
                if users_model().update_pwrecovery_status(username):
                    raise web.seeother('/login')
                else:
                    return 'Database error.'
            else:
                return 'Database error - password not updated.'
        else:
            raise web.seeother('/login')
