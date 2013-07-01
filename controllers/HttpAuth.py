__author__ = 'zcabh_000'
import web


class Auth:

    def GET(self):
        if web.ctx.env.get('HTTP_AUTHORIZATION') == None:
            web.ctx.status = '401 Unauthorized'
        else:
            return "Authorized"