import web
from libraries.utils import hash_utils
from models.users import users_model
from environment import render_private as render


class pwrequest:

    def GET(self):
        return render.pwrequest()

    def POST(self):
        username = web.input().Username
        rand = hash_utils.random_hex(username)
        user_email = users_model.request_password(username, rand)
        if user_email == '':
            return "User was not found!"
        else:
            web.config.smtp_server = 'smtp.gmail.com'
            web.config.smtp_port = 587
            web.config.smtp_username = 'sprkssuprt@gmail.com'
            web.config.smtp_password = 'sprks123456789'
            web.config.smtp_starttls = True
            web.sendmail('support', user_email, 'Password recovery', 'http://localhost:8080/pwrecovery/'+rand)
            return "Email sent"
