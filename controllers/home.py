from localsys.environment import render
from models.users import users_model
from libraries.user_helper import authenticate


class home:

    def GET(self):
        return render.home()
